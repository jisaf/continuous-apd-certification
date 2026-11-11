import json
import shutil
import warnings

import openpyxl
import pytest

from capd import package
from capd.cli import main
from capd.validators import sirt, templates

from .conftest import ROOT

SAMPLE = ROOT / "examples/sample-package/fna-uat"


def copy_sample(tmp_path):
    dst = tmp_path / "fna-uat"
    shutil.copytree(SAMPLE, dst)
    return dst


def edit(path, fn):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        wb = openpyxl.load_workbook(path)
    fn(wb)
    wb.save(path)


def test_pinned_sirt_template_is_identified_and_blank_rows_are_errors(catalog):
    with __import__("importlib").resources.as_file(templates.pinned_path("sirt")) as p:
        assert templates.identify(p) == "sirt"
        r = sirt.validate(p, catalog)
    assert r["rows"] == 821 and r["answered"] < 100
    assert "Eligibility (A and B) row 4 (AP-1, fna:sirt:S0001): no answer" in r["errors"]


def test_sample_sirt_response_passes(catalog):
    r = sirt.validate(SAMPLE / "sirt-response.xlsx", catalog)
    assert r["errors"] == [] and r["answered"] == 821


def test_no_without_reason_and_moved_rows(tmp_path, catalog):
    p = copy_sample(tmp_path) / "sirt-response.xlsx"

    def change(wb):
        ws = wb["Eligibility (A and B)"]
        ws["D5"] = "N"           # AP-2, no reason
        ws["F5"] = None
        ws["D6"] = None          # AP-3 unanswered
        ws.insert_rows(10)       # moves every row below
    edit(p, change)
    errs = sirt.validate(p, catalog)["errors"]
    assert any("AP-2" in e and "without a reason" in e for e in errs)
    assert any("AP-3" in e and "no answer" in e for e in errs)
    assert any("rows were added, removed, or moved" in e for e in errs)


def test_unknown_template_version_is_refused(tmp_path, catalog):
    p = copy_sample(tmp_path) / "sirt-response.xlsx"
    edit(p, lambda wb: wb["Claims (C)"].cell(1, 1, "Identifier"))
    r = sirt.validate(p, catalog)
    assert r["template"] is None and "unknown SIRT template version" in r["errors"][0]


def test_yes_answer_on_failing_rule_warns(catalog):
    bundle = {"records": [{"kind": "test", "result": "fail", "ruleIds": ["fna:sirt:S0215"]}]}
    r = sirt.validate(SAMPLE / "sirt-response.xlsx", catalog, bundle)
    assert r["errors"] == [] and len(r["warnings"]) == 1 and "OD-1" in r["warnings"][0]


def test_package_record_lists_missing_items_and_hashes_files(tmp_path, catalog):
    d = copy_sample(tmp_path)
    rec = package.build(d, "FNA-UAT", catalog)
    by_key = {c["key"]: c for c in rec["checklist"]}
    assert by_key["fna:golive:GL08"]["status"] == "present"
    assert by_key["fna:golive:GL02"]["status"] == "missing"
    assert rec["summary"]["present"] == 6 and not rec["summary"]["complete"]
    assert rec["workbooks"][0]["kind"] == "sirt" and rec["workbooks"][0]["errors"] == []
    assert {f["path"] for f in rec["files"]} >= {"sirt-response.xlsx", "letters/transmittal-letter.md"}
    assert not any(c["key"].startswith("fna:sirt:") for c in rec["checklist"])
    assert package.verify(rec, d) == []

    (d / "letters/transmittal-letter.md").write_text("changed")
    assert package.verify(rec, d) == ["letters/transmittal-letter.md: changed since the record was made"]
    rec["summary"]["missing"] = 0
    assert "recordSha256 does not match" in package.verify(rec)[0]


def test_package_missing_workbook_and_listed_file(tmp_path, catalog):
    d = copy_sample(tmp_path)
    (d / "sirt-response.xlsx").unlink()
    rec = package.build(d, "FNA-UAT", catalog)
    assert rec["workbooks"][0]["errors"] == ["no SIRT response workbook in the package"]
    gl08 = next(c for c in rec["checklist"] if c["key"] == "fna:golive:GL08")
    assert gl08["status"] == "missing" and gl08["missingFiles"] == ["sirt-response.xlsx"]


def test_package_complete_when_every_item_has_a_file(tmp_path, catalog):
    d = copy_sample(tmp_path)
    items = {}
    for r in package.checklist_rules(catalog, "FNA-UAT"):
        f = f"docs/{r['sourceId']}.md"
        (d / f).parent.mkdir(exist_ok=True)
        (d / f).write_text(r["title"])
        items[r["key"]] = [f]
    items["fna:golive:GL08"].append("sirt-response.xlsx")
    (d / "package.yaml").write_text(json.dumps({"gate": "FNA-UAT", "items": items}))
    assert package.build(d, "FNA-UAT", catalog)["summary"]["complete"]


def test_package_index_errors(tmp_path, catalog):
    d = copy_sample(tmp_path)
    with pytest.raises(ValueError, match="is for gate FNA-UAT"):
        package.build(d, "ORR", catalog)
    (d / "package.yaml").write_text("items: {fna:golive:GL99: [x.md]}")
    with pytest.raises(ValueError, match="unknown rule key"):
        package.build(d, "FNA-UAT", catalog)


def test_cli_package_check_and_verify(tmp_path, capsys):
    out = tmp_path / "out"
    assert main(["package", "check", "FNA-UAT", str(SAMPLE), "-o", str(out)]) == 1   # not complete
    assert (out / "checklist.md").read_text().startswith("# FNA-UAT package checklist")
    assert main(["package", "verify", str(out / "submission-record.json"), str(SAMPLE)]) == 0
    assert main(["validate", "sirt", str(SAMPLE / "sirt-response.xlsx")]) == 0
    assert "submission record verified" in capsys.readouterr().out
