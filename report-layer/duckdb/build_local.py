"""Build the report layer locally in DuckDB: no Snowflake account needed.

    pip install -e ".[dev]"            # from the repository root (installs capd and duckdb)
    python report-layer/duckdb/build_local.py --evidence "out/demo/*/evidence-rows.ndjson"

Creates out/report-layer/cert.duckdb with the same tables and views as the Snowflake template, loads the
capd catalog, pipeline evidence, the sample tracked items / acceptances / gates / defects, and synthetic
metric-contract data, then runs the reference metric queries. Open it with the dashboard
(report-layer/dashboard/app.py), the DuckDB CLI, or any BI tool with a DuckDB driver.
"""

from __future__ import annotations

import argparse
import glob
import random
from datetime import datetime, timedelta
from pathlib import Path

import duckdb

from capd.catalog import Catalog

HERE = Path(__file__).resolve().parent
LAYER = HERE.parent
SQL = LAYER / "sql"


def statements(path: Path) -> list[str]:
    """Split a SQL file into statements after removing full-line comments."""
    text = "\n".join(ln for ln in path.read_text().splitlines() if not ln.strip().startswith("--"))
    return [s.strip() for s in text.split(";") if s.strip()]


def run_sql_file(con, path: Path) -> None:
    for stmt in statements(path):
        con.execute(stmt)


def load_catalog(con, catalog: Catalog) -> None:
    con.execute("DELETE FROM RULES")
    con.execute("DELETE FROM RULE_GATES")
    con.executemany("INSERT INTO RULES VALUES (?,?,?,?,?,?,?,?,?,?,?)", [
        (r["key"], r["agency"], r["set"], r["sourceId"], r["title"], r["responsibility"], r["coverage"],
         r["acceptance"], r["freshnessDays"], ",".join(r["programs"]), r.get("applicable", True))
        for r in catalog.rules.values()])
    con.executemany("INSERT INTO RULE_GATES VALUES (?,?,?)", [
        (r["key"], gate, kind) for r in catalog.rules.values() for gate, kinds in r["gates"].items() for kind in kinds])


def load_evidence(con, patterns: list[str]) -> int:
    files = sorted({f for p in patterns for f in glob.glob(p)})
    for f in files:
        con.execute("INSERT INTO EVIDENCE SELECT * FROM read_json(?, format='newline_delimited', columns={"
                    "build_id:'VARCHAR', commit_sha:'VARCHAR', branch:'VARCHAR', generated_at:'TIMESTAMP',"
                    "catalog_version:'VARCHAR', rule_key:'VARCHAR', kind:'VARCHAR', result:'VARCHAR', value:'DOUBLE',"
                    "unit:'VARCHAR', programs:'VARCHAR', environment:'VARCHAR', executed_by:'VARCHAR', test_id:'VARCHAR',"
                    "name:'VARCHAR', observed_at:'TIMESTAMP', source_uri:'VARCHAR'})", [f])
    return len(files)


def load_csvs(con, folder: Path) -> None:
    for table in ("TRACKED_ITEMS", "ACCEPTANCES", "GATES", "DEFECTS"):
        f = folder / f"{table.lower()}.csv"
        if f.exists():
            con.execute(f"DELETE FROM {table}")
            con.execute(f"INSERT INTO {table} BY NAME SELECT * FROM read_csv_auto(?, header=true)", [str(f)])


def synthetic(con, months: int = 6, seed: int = 7) -> None:
    """Deterministic synthetic data for the metric contract (no real people or cases)."""
    rnd = random.Random(seed)
    start = datetime(2026, 5, 1)
    apps, dets, notices, renewals, work = [], [], [], [], []
    for i in range(1, months * 400 + 1):
        received = start + timedelta(days=rnd.randrange(months * 30), hours=rnd.randrange(24))
        programs = rnd.choice(["medicaid", "snap", "medicaid,snap"])
        expedited = "snap" in programs and rnd.random() < 0.2
        app_id = f"APP{i:06d}"
        apps.append((app_id, received, rnd.choice(["online", "online", "phone", "paper", "in_person"]), programs, expedited))
        for prog in programs.split(","):
            days = rnd.choice([1, 3, 5, 8, 12, 20, 28, 33, 50]) if prog == "snap" else rnd.choice([1, 2, 10, 30, 44, 60, 95])
            method = "SNAP" if prog == "snap" else rnd.choice(["MAGI", "MAGI", "MAGI", "non-MAGI"])
            decided = received + timedelta(days=days)
            dets.append((app_id, prog, rnd.choice(["approved", "approved", "denied"]), decided, rnd.random() < 0.62, method))
            notices.append((f"N{i:06d}{prog[0]}", app_id, "eligibility", rnd.choice(["mail", "email", "portal"]),
                            decided, decided + timedelta(days=rnd.choice([0, 0, 1, 2])), rnd.random() < 0.85))
    for i in range(1, months * 150 + 1):
        due = (start + timedelta(days=rnd.randrange(months * 30))).date()
        renewals.append((f"R{i:05d}", "medicaid", due, datetime.combine(due, datetime.min.time()) - timedelta(days=rnd.randrange(20)),
                         rnd.random() < 0.55, rnd.random() < 0.9))
    for i in range(1, 301):
        created = start + timedelta(days=rnd.randrange(months * 30))
        work.append((f"W{i:05d}", rnd.choice(["initial", "recertification", "change_report"]), created,
                     rnd.choice(["open", "closed", "closed"]), (created + timedelta(days=30)).date()))
    for table in ("C_APPLICATION", "C_DETERMINATION", "C_NOTICE", "C_RENEWAL", "C_WORK_ITEM"):
        con.execute(f"DELETE FROM {table}")
    con.executemany("INSERT INTO C_APPLICATION VALUES (?,?,?,?,?)", apps)
    con.executemany("INSERT INTO C_DETERMINATION VALUES (?,?,?,?,?,?)", dets)
    con.executemany("INSERT INTO C_NOTICE VALUES (?,?,?,?,?,?,?)", notices)
    con.executemany("INSERT INTO C_RENEWAL VALUES (?,?,?,?,?,?)", renewals)
    con.executemany("INSERT INTO C_WORK_ITEM VALUES (?,?,?,?,?)", work)


def run_metrics(con, out: Path) -> dict[str, int]:
    out.mkdir(parents=True, exist_ok=True)
    results = {}
    for f in sorted((SQL / "metrics").glob("*.sql")):
        rel = con.execute(f.read_text().rstrip().rstrip(";"))
        rows = rel.fetchall()
        cols = [d[0] for d in rel.description]
        with open(out / f"{f.stem}.csv", "w") as fh:
            fh.write(",".join(cols) + "\n")
            for r in rows:
                fh.write(",".join("" if v is None else str(v) for v in r) + "\n")
        results[f.stem] = len(rows)
    return results


def build(db: str, evidence: list[str], sample_data: Path | None, with_synthetic: bool = True) -> duckdb.DuckDBPyConnection:
    Path(db).parent.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect(db)
    for f in (SQL / "10_tables.sql", HERE / "10_schema.sql", SQL / "20_metric_contract.sql"):
        run_sql_file(con, f)
    load_catalog(con, Catalog.load())
    con.execute("DELETE FROM EVIDENCE")
    load_evidence(con, evidence)
    if sample_data:
        load_csvs(con, sample_data)
    if with_synthetic:
        synthetic(con)
    run_sql_file(con, SQL / "30_views.sql")
    return con


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--db", default="out/report-layer/cert.duckdb")
    ap.add_argument("--evidence", nargs="+", default=["out/demo/*/evidence-rows.ndjson"])
    ap.add_argument("--sample-data", default=str(LAYER / "sample-data"))
    ap.add_argument("--no-synthetic", action="store_true")
    args = ap.parse_args()
    con = build(args.db, args.evidence, Path(args.sample_data) if args.sample_data else None, not args.no_synthetic)
    metrics = run_metrics(con, Path(args.db).parent / "metrics")
    print(f"built {args.db}")
    print("rule status by gate:")
    for gate, status, n in con.execute("SELECT gate, status, COUNT(*) FROM V_RULE_STATUS GROUP BY 1, 2 ORDER BY 1, 2").fetchall():
        print(f"  {gate:<10} {status:<20} {n}")
    blockers = con.execute("SELECT COUNT(*) FROM V_GATE_BLOCKERS").fetchone()[0]
    print(f"gate blockers: {blockers} (see V_GATE_BLOCKERS)")
    print("metric queries:", ", ".join(f"{k} ({v} rows)" for k, v in metrics.items()))


if __name__ == "__main__":
    main()
