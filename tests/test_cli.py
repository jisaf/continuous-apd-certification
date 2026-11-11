import json
import shutil

import yaml

from capd.cli import main

from .conftest import FIX


def write_config(tmp_path, **extra):
    shutil.copy(FIX / "junit.xml", tmp_path / "junit.xml")
    shutil.copy(FIX / "security.sarif", tmp_path / "security.sarif")
    cfg = {"catalogVersion": "1.0.0", "sources": [{"connector": "junit", "paths": ["junit.xml"]},
                                                 {"connector": "sarif", "paths": ["security.sarif"]}],
           "sinks": [{"connector": "file", "options": {"dir": "out-files"}}]}
    cfg.update(extra)
    (tmp_path / "capd.yaml").write_text(yaml.safe_dump(cfg))
    return tmp_path / "capd.yaml"


def test_run_end_to_end(tmp_path):
    cfg = write_config(tmp_path)
    assert main(["run", "--config", str(cfg), "--out-dir", str(tmp_path / "out"), "--build-id", "7", "--commit", "c" * 40,
                 "--branch", "main"]) == 0
    for f in ("bundle.json", "comparison.json", "summary.md", "report.html"):
        assert (tmp_path / "out" / f).exists()
    assert (tmp_path / "out-files" / "evidence-rows.ndjson").exists()
    assert json.loads((tmp_path / "out" / "bundle.json").read_text())["build"]["id"] == "7"


def test_blocking_gate_fails_on_regression(tmp_path):
    cfg = write_config(tmp_path, gateMode="blocking")
    out = tmp_path / "out"
    assert main(["collect", "--config", str(cfg), "-o", str(out / "base.json"), "--build-id", "1", "--branch", "main"]) == 0
    xml = (tmp_path / "junit.xml").read_text().replace(
        'name="test_standard_deduction" time="0.010">', 'name="test_standard_deduction" time="0.010"><failure message="x"/>')
    (tmp_path / "junit.xml").write_text(xml)
    assert main(["collect", "--config", str(cfg), "-o", str(out / "cur.json"), "--build-id", "2"]) == 0
    code = main(["compare", "--config", str(cfg), "--bundle", str(out / "cur.json"), "--baseline", str(out / "base.json"),
                 "-o", str(out / "cmp.json"), "--markdown", str(out / "s.md")])
    assert code == 1 and json.loads((out / "cmp.json").read_text())["blocking"]


def test_check_tags_exit_code(tmp_path):
    cfg = write_config(tmp_path)
    main(["collect", "--config", str(cfg), "-o", str(tmp_path / "b.json")])
    assert main(["check-tags", "--config", str(cfg), "--bundle", str(tmp_path / "b.json")]) == 1   # EE999 is unknown


def test_catalog_pin_is_enforced(tmp_path, capsys):
    cfg = write_config(tmp_path, catalogVersion="0.9.0")
    try:
        main(["collect", "--config", str(cfg), "-o", str(tmp_path / "b.json")])
        raise AssertionError("pin not enforced")
    except SystemExit as e:
        assert "change control" in str(e)


def test_validate_and_catalog_commands(capsys):
    assert main(["validate", "templates"]) == 1          # CMS template and rules disagree today
    assert main(["catalog", "--search", "standard deduction"]) == 0
    assert "fna:sirt:S0215" in capsys.readouterr().out
    assert main(["connectors"]) == 0


def test_mapping_views_and_check(capsys, tmp_path):
    from .conftest import ROOT
    path = ROOT / "templates" / "config" / "mapping.yaml"
    assert main(["mapping", "views", str(path)]) == 0
    sql = capsys.readouterr().out
    assert "CREATE OR REPLACE VIEW C_APPLICATION AS" in sql
    assert "CASE SUBMIT_CHANNEL_CD WHEN 'WEB' THEN 'online'" in sql
    assert "WHERE PGM_CD = 'MA'" in sql
    assert main(["mapping", "check", str(path)]) == 0
    result = json.loads(capsys.readouterr().out)
    assert "appeal_transfer.record_id" in result["unmapped"]
    assert "golive_backlog (GL10)" in result["readyMetrics"] and not result["blockedMetrics"]
    partial = tmp_path / "m.yaml"
    partial.write_text("records:\n  notice:\n    table: T\n    fields: { generated_at: G }\n")
    main(["mapping", "check", str(partial)])
    assert json.loads(capsys.readouterr().out)["blockedMetrics"]["ee09_automated_notices (EE9)"] == ["notice.automatic"]
