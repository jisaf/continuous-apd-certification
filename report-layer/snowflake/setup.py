"""Set up the report layer on a Snowflake account in one step, and check it against the DuckDB reference.

    pip install "capd[snowflake]" duckdb
    export SNOWFLAKE_ACCOUNT=... SNOWFLAKE_USER=... SNOWFLAKE_PASSWORD=...   # or SNOWFLAKE_PRIVATE_KEY_PATH
    python report-layer/snowflake/setup.py --warehouse COMPUTE_WH \
        --evidence "out/demo/*/bundle.json" --sample-data --synthetic --compare-duckdb

Runs, in order: 10_schema.sql, ../sql/10_tables.sql, ../sql/20_metric_contract.sql (with --synthetic),
loads the catalog, the evidence bundles (through the capd snowflake sink's statements), the sample state
data, and synthetic metric data, then ../sql/30_views.sql and 20_roles.sql. With --compare-duckdb it builds
the same data in DuckDB and checks that V_RULE_STATUS and V_GATE_BLOCKERS agree row for row.

Use a role that can create databases and roles (for a trial account, ACCOUNTADMIN). Without --sample-data
and --synthetic it sets up an empty layer for the state's own data. --fake runs on fakesnow, a local
imitation of Snowflake, for a first check without an account (it skips 20_roles.sql).
"""

from __future__ import annotations

import argparse
import csv
import glob
import importlib.util
import json
import os
import sys
from pathlib import Path

from capd.catalog import Catalog
from capd.connectors.snowflake import SnowflakeSink

HERE = Path(__file__).resolve().parent
LAYER = HERE.parent
SQL = LAYER / "sql"
DB, SCHEMA = "CERTIFICATION", "CERT"
SAMPLE_TABLES = ("TRACKED_ITEMS", "ACCEPTANCES", "GATES", "DEFECTS")


def _local():
    spec = importlib.util.spec_from_file_location("build_local", LAYER / "duckdb" / "build_local.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class Conn:
    """Small adapter: '?' placeholders (as in build_local.py) on a Snowflake connection."""

    def __init__(self, con):
        self.con = con
        self.cur = con.cursor()

    def execute(self, sql, params=None):
        self.cur.execute(sql.replace("?", "%s"), params)
        return self.cur

    def executemany(self, sql, rows):
        rows = list(rows)
        for i in range(0, len(rows), 1000):
            self.cur.executemany(sql.replace("?", "%s"), rows[i:i + 1000])

    def rows(self, sql):
        return [tuple(r) for r in self.execute(sql).fetchall()]


def statements(path: Path) -> list[str]:
    text = "\n".join(ln for ln in path.read_text().splitlines() if not ln.strip().startswith("--"))
    return [s.strip() for s in text.split(";") if s.strip()]


def run_file(c: Conn, path: Path) -> None:
    for stmt in statements(path):
        c.execute(stmt)
    print(f"ran {path.relative_to(LAYER)}")


def load_csv(c: Conn, table: str, path: Path) -> int:
    with path.open(newline="") as fh:
        rows = list(csv.DictReader(fh))
    if not rows:
        return 0
    cols = list(rows[0])
    c.execute(f"DELETE FROM {table}")
    c.executemany(f"INSERT INTO {table} ({', '.join(cols)}) VALUES ({', '.join('?' * len(cols))})",
                  [[r[k] if r[k] != "" else None for k in cols] for r in rows])
    return len(rows)


def load_bundles(c: Conn, patterns: list[str]) -> int:
    files = sorted({f for p in patterns for f in glob.glob(p)})
    sink = SnowflakeSink()
    for f in files:
        for sql, params in sink.statements(json.loads(Path(f).read_text()), {"database": DB, "schema": SCHEMA}):
            c.cur.execute(sql, params)
    return len(files)


def connect(args):
    if args.fake:
        import fakesnow  # noqa: F401  (local imitation of Snowflake on DuckDB)
        import snowflake.connector

        args._patch = fakesnow.patch()
        args._patch.__enter__()
        return snowflake.connector.connect(database=DB, schema=SCHEMA)
    import snowflake.connector

    kwargs = {"account": os.environ["SNOWFLAKE_ACCOUNT"], "user": os.environ["SNOWFLAKE_USER"],
              "warehouse": args.warehouse, "role": args.role}
    if os.environ.get("SNOWFLAKE_PRIVATE_KEY_PATH"):
        kwargs["private_key_file"] = os.environ["SNOWFLAKE_PRIVATE_KEY_PATH"]
    else:
        kwargs["password"] = os.environ["SNOWFLAKE_PASSWORD"]
    return snowflake.connector.connect(**{k: v for k, v in kwargs.items() if v})


def compare_with_duckdb(c: Conn, args) -> list[str]:
    local = _local()
    ndjson = []
    tmp = Path("out/report-layer/compare")
    tmp.mkdir(parents=True, exist_ok=True)
    from capd.connectors.file_sink import rows as evidence_rows

    for i, f in enumerate(sorted({f for p in args.evidence for f in glob.glob(p)})):
        p = tmp / f"rows-{i}.ndjson"
        p.write_text("".join(json.dumps(r) + "\n" for r in evidence_rows(json.loads(Path(f).read_text()))))
        ndjson.append(str(p))
    duck = local.build(str(tmp / "compare.duckdb"), ndjson, LAYER / "sample-data" if args.sample_data else None,
                       args.synthetic)
    problems = []
    for view, cols in (("V_RULE_STATUS", "gate, rule_key, status"),
                       ("V_GATE_BLOCKERS", "gate, reason, item")):
        q = f"SELECT {cols} FROM {view} ORDER BY {cols}"
        sf = [tuple(str(v) for v in r) for r in c.rows(q)]
        dk = [tuple(str(v) for v in r) for r in duck.execute(q).fetchall()]
        if sf != dk:
            only_sf, only_dk = set(sf) - set(dk), set(dk) - set(sf)
            problems.append(f"{view}: {len(sf)} rows on Snowflake, {len(dk)} on DuckDB; "
                            f"only on Snowflake {sorted(only_sf)[:5]}, only on DuckDB {sorted(only_dk)[:5]}")
        else:
            print(f"{view}: {len(sf)} rows, same on Snowflake and DuckDB")
    return problems


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--warehouse"), ap.add_argument("--role", default="ACCOUNTADMIN")
    ap.add_argument("--evidence", nargs="*", default=[], help="evidence bundle files or globs (bundle.json)")
    ap.add_argument("--sample-data", action="store_true", help="load report-layer/sample-data")
    ap.add_argument("--synthetic", action="store_true", help="create the metric contract tables with synthetic data")
    ap.add_argument("--skip-roles", action="store_true")
    ap.add_argument("--compare-duckdb", action="store_true")
    ap.add_argument("--fake", action="store_true", help="run on fakesnow instead of a Snowflake account")
    args = ap.parse_args(argv)

    c = Conn(connect(args))
    run_file(c, HERE / "10_schema.sql")
    c.execute(f"USE SCHEMA {DB}.{SCHEMA}")
    run_file(c, SQL / "10_tables.sql")
    if args.synthetic:
        run_file(c, SQL / "20_metric_contract.sql")
    _local().load_catalog(c, Catalog.load())
    print(f"loaded catalog ({c.rows('SELECT COUNT(*) FROM RULES')[0][0]} rules)")
    c.execute("DELETE FROM EVIDENCE")
    print(f"loaded {load_bundles(c, args.evidence)} evidence bundle(s) through the snowflake sink "
          f"({c.rows('SELECT COUNT(*) FROM EVIDENCE')[0][0]} rows)")
    if args.sample_data:
        for t in SAMPLE_TABLES:
            print(f"loaded {load_csv(c, t, LAYER / 'sample-data' / f'{t.lower()}.csv')} rows into {t}")
    if args.synthetic:
        _local().synthetic(c)
        print("loaded synthetic metric contract data")
    run_file(c, SQL / "30_views.sql")
    if not (args.skip_roles or args.fake):
        run_file(c, HERE / "20_roles.sql")
        c.execute(f"USE SCHEMA {DB}.{SCHEMA}")
    if args.synthetic:
        for f in sorted((SQL / "metrics").glob("*.sql")):
            print(f"metric {f.stem}: {len(c.execute(f.read_text().rstrip().rstrip(';')).fetchall())} rows")
    for gate, status, n in c.rows("SELECT gate, status, COUNT(*) FROM V_RULE_STATUS GROUP BY 1, 2 ORDER BY 1, 2"):
        print(f"  {gate:<10} {status:<20} {n}")
    problems = compare_with_duckdb(c, args) if args.compare_duckdb else []
    for p in problems:
        print(f"MISMATCH {p}", file=sys.stderr)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
