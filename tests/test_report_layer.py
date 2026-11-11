"""The report layer's SQL (run here on DuckDB) must agree with the Python reference status logic."""

import json
from datetime import date

import pytest

from capd.status import evaluate

from .conftest import ROOT, load_module

duckdb = pytest.importorskip("duckdb")
local = load_module("build_local", ROOT / "report-layer" / "duckdb" / "build_local.py")
queries = load_module("queries", ROOT / "report-layer" / "dashboard" / "queries.py")

RULES = {
    "cms:ee:EE5": {"gates": {"ORR": ["test"], "CR": ["metric"]}, "freshnessDays": 30, "acceptance": "not_required"},
    "cms:ee:EE6": {"gates": {"ORR": ["test"]}, "freshnessDays": 30, "acceptance": "not_required"},
    "cms:ee:EE9": {"gates": {"ORR": ["test"]}, "freshnessDays": 30, "acceptance": "not_required"},
    "cms:cef:CEF09": {"gates": {"ORR": ["attestation"]}, "freshnessDays": 365, "acceptance": "required"},
    "cms:cef:CEF12": {"gates": {"ORR": ["attestation"]}, "freshnessDays": 365, "acceptance": "required"},
    "cms:cef:CEF20": {"gates": {"ORR": ["document"]}, "freshnessDays": 365, "acceptance": "required"},
    "cms:ee:EE12": {"gates": {"ORR": ["test"]}, "freshnessDays": 30, "acceptance": "not_required"},
}
TODAY = date.today().isoformat()


def ev(rule, kind, result, observed, env="ci", build="m2", branch="main", test="t"):
    return {"build_id": build, "commit_sha": "c", "branch": branch, "generated_at": f"{observed} 00:00:00",
            "catalog_version": "1.0.0", "rule_key": rule, "kind": kind, "result": result, "value": None, "unit": None,
            "programs": "medicaid", "environment": env, "executed_by": "automation", "test_id": f"{rule}-{test}",
            "name": None, "observed_at": f"{observed} 00:00:00", "source_uri": "x"}


@pytest.fixture
def db(tmp_path):
    con = duckdb.connect(str(tmp_path / "t.duckdb"))
    for f in (local.SQL / "10_tables.sql", local.HERE / "10_schema.sql", local.SQL / "20_metric_contract.sql"):
        local.run_sql_file(con, f)
    for key, r in RULES.items():
        con.execute("INSERT INTO RULES VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                    [key, key.split(":")[0], key.split(":")[1], key.split(":")[2], key, "vendor", "evidenced",
                     r["acceptance"], r["freshnessDays"], "medicaid", True])
        for g, kinds in r["gates"].items():
            for k in kinds:
                con.execute("INSERT INTO RULE_GATES VALUES (?,?,?)", [key, g, k])
    rows = [
        ev("cms:ee:EE5", "test", "pass", TODAY),
        ev("cms:ee:EE6", "test", "pass", TODAY), ev("cms:ee:EE6", "test", "fail", TODAY, test="u"),
        ev("cms:ee:EE9", "test", "pass", "2026-01-01", build="m1"),          # older main build: ignored
        ev("cms:ee:EE5", "metric", "value", TODAY, env="production"),
        ev("cms:ee:EE12", "test", "pass", TODAY),
    ]
    p = tmp_path / "rows.ndjson"
    p.write_text("".join(json.dumps(r) + "\n" for r in rows))
    local.load_evidence(con, [str(p)])
    con.execute("UPDATE EVIDENCE SET generated_at = TIMESTAMP '2026-01-01' WHERE build_id = 'm1'")
    con.execute("INSERT INTO TRACKED_ITEMS VALUES ('a','cms:cef:CEF09','ORR','attestation','SAR','sec',NULL,'complete','present', "
                f"TIMESTAMP '{TODAY} 00:00:00', NULL, NULL)")
    con.execute("INSERT INTO TRACKED_ITEMS VALUES ('b','cms:cef:CEF12','ORR','attestation','508','v',NULL,'complete','present', "
                "TIMESTAMP '2020-01-01 00:00:00', NULL, NULL)")
    con.execute(f"INSERT INTO ACCEPTANCES VALUES ('cms:cef:CEF09','ORR','accepted','sec', TIMESTAMP '{TODAY} 00:00:00', NULL)")
    con.execute(f"INSERT INTO ACCEPTANCES VALUES ('cms:ee:EE12','ORR','na_accepted','dir', TIMESTAMP '{TODAY} 00:00:00', NULL)")
    con.execute("INSERT INTO GATES VALUES ('ORR', DATE '2099-01-01', 'pilot-is-medicaid-go-live')")
    local.run_sql_file(con, local.SQL / "30_views.sql")
    return con


def python_status(rule, gate):
    r = RULES[rule]
    evid = {
        "cms:ee:EE5": [{"kind": "test", "result": "pass", "observedAt": TODAY, "environment": "ci"},
                       {"kind": "metric", "result": "value", "observedAt": TODAY, "environment": "production"}],
        "cms:ee:EE6": [{"kind": "test", "result": "pass", "observedAt": TODAY}, {"kind": "test", "result": "fail", "observedAt": TODAY}],
        "cms:ee:EE9": [],
        "cms:cef:CEF09": [{"kind": "attestation", "result": "present", "observedAt": TODAY}],
        "cms:cef:CEF12": [{"kind": "attestation", "result": "present", "observedAt": "2020-01-01"}],
        "cms:cef:CEF20": [],
        "cms:ee:EE12": [{"kind": "test", "result": "pass", "observedAt": TODAY}],
    }[rule]
    gate_date = "2099-01-01" if gate == "ORR" else None
    return evaluate(r, gate, evid, as_of=TODAY, gate_date=gate_date, accepted=rule == "cms:cef:CEF09",
                    na_accepted=rule == "cms:ee:EE12" and gate == "ORR")


def test_sql_status_matches_python(db):
    got = {(k, g): s for k, g, s in db.execute("SELECT rule_key, gate, status FROM V_RULE_STATUS").fetchall()}
    expected = {(k, g): python_status(k, g) for k, r in RULES.items() for g in r["gates"]}
    assert got == expected
    # sanity: the cases cover the interesting statuses
    assert {"Met", "Not met", "No evidence", "Stale", "N/A"} <= set(got.values())


def test_blockers_are_a_list_and_calendar(db):
    reasons = {r for (r,) in db.execute("SELECT DISTINCT reason FROM V_GATE_BLOCKERS").fetchall()}
    assert {"Not met", "No evidence", "Stale"} <= reasons
    assert db.execute("SELECT COUNT(*) FROM V_CALENDAR").fetchone()[0] >= 1


def test_metric_queries_run_on_synthetic_data(tmp_path):
    con = local.build(str(tmp_path / "m.duckdb"), [], None, True)
    res = local.run_metrics(con, tmp_path / "metrics")
    assert set(res) >= {"ee05_automated_determinations", "ee06_timeliness", "golive_snap_timeliness", "golive_backlog"}
    for metric in ("ee05_automated_determinations", "ee06_timeliness", "ee09_automated_notices", "golive_snap_timeliness"):
        lines = (tmp_path / "metrics" / f"{metric}.csv").read_text().splitlines()
        assert lines[0] == "metric_id,period_month,numerator,denominator,value" and len(lines) > 2
        assert all(0 <= float(ln.split(",")[-1]) <= 100 for ln in lines[1:])


def test_dashboard_queries_run(db):
    for name in ("STATUS_BY_GATE", "BLOCKER_COUNTS", "CALENDAR", "TRENDS", "TIME_TO_RESTORE", "GATES"):
        cols, _ = queries.run(db, getattr(queries, name))
        assert cols
    cols, rows = queries.run(db, queries.BLOCKERS, ["ORR"])
    assert rows and cols[0] == "gate"
