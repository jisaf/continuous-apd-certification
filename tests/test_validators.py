import shutil
import warnings

import openpyxl

from capd.validators import intake, orw, templates


def copy_orw(tmp_path, name="Operational_Workbook_ST_EE_2026-10-31.xlsx"):
    dst = tmp_path / name
    with __import__("importlib").resources.as_file(templates.pinned_path("orw")) as p:
        shutil.copy(p, dst)
    return dst


def edit(path, fn):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        wb = openpyxl.load_workbook(path)
    fn(wb)
    wb.save(path)


def test_cms_sample_orw_passes(tmp_path):
    r = orw.validate(copy_orw(tmp_path))
    assert r["errors"] == [] and r["template"].startswith("CMS ORW template")


def test_filename_and_field_rules(tmp_path):
    p = copy_orw(tmp_path, "orw.xlsx")
    edit(p, lambda wb: wb["Metric Definitions"].cell(row=3, column=3, value="EE1|ST-EE-01"))
    errs = orw.validate(p)["errors"]
    assert any("_YYYY-MM-DD" in e for e in errs)
    assert any("ST-EE-01" in e and "STEE01" in e for e in errs)


def test_merged_cells_and_unknown_template(tmp_path):
    p = copy_orw(tmp_path)
    edit(p, lambda wb: wb["Metric Values"].merge_cells("A3:B3"))
    assert any("merged cells" in e for e in orw.validate(p)["errors"])
    q = copy_orw(tmp_path, "Operational_Workbook_ST_EE_2026-11-30.xlsx")
    edit(q, lambda wb: wb["Metric Definitions"].cell(row=1, column=9, value="Extra Column"))
    r = orw.validate(q)
    assert r["template"] is None and "unknown ORW template version" in r["errors"][0]


def test_cms_template_and_rules_disagree_and_we_detect_it():
    diffs = templates.orw_rules_conformance()
    assert any("Metric Reporting Frequency" in d for d in diffs)
    assert any("OAPD Metric Status" in d for d in diffs)


def test_intake_form(tmp_path, catalog):
    with __import__("importlib").resources.as_file(templates.pinned_path("intake")) as p:
        dst = tmp_path / "intake.xlsx"
        shutil.copy(p, dst)
    assert intake.validate(dst, catalog)["errors"] == []

    def break_it(wb):
        ws = wb["Outcomes & Metrics"]
        for row in ws.iter_rows(min_row=3):
            if row[0].value and str(row[0].value).startswith("EE21"):
                row[0].value = None
        ws.cell(row=4, column=6, value="N/A")
    edit(dst, break_it)
    errs = intake.validate(dst, catalog)["errors"]
    assert any("EE21 is missing" in e for e in errs)
    assert any("N/A without a justification" in e for e in errs)
