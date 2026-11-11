"""Sink connector: load a run's evidence into the report layer on Snowflake.

Inserts the bundle into CERT.BUNDLES and one row per (record, rule key) into CERT.EVIDENCE, the tables
created by report-layer/snowflake/10_schema.sql. Install with: pip install "capd[snowflake]".
Credentials come from environment variables (SNOWFLAKE_ACCOUNT, SNOWFLAKE_USER, and SNOWFLAKE_PRIVATE_KEY_PATH
or SNOWFLAKE_PASSWORD), set as pipeline secrets for the write-only loader role.
Any other SQL platform can load the NDJSON written by the file sink instead.
"""

from __future__ import annotations

import json
import os

from .file_sink import rows

COLUMNS = ["build_id", "commit_sha", "branch", "generated_at", "catalog_version", "rule_key", "kind", "result",
           "value", "unit", "programs", "environment", "executed_by", "test_id", "name", "observed_at", "source_uri"]


class SnowflakeSink:
    id = "snowflake"
    config_schema = {"type": "object", "properties": {"database": {"type": "string"}, "schema": {"type": "string"},
                                                      "warehouse": {"type": "string"}, "role": {"type": "string"}}}

    def statements(self, bundle: dict, options: dict) -> list[tuple[str, list]]:
        db, sch = options.get("database", "CERTIFICATION"), options.get("schema", "CERT")
        b = bundle["build"]
        stmts = [(f"DELETE FROM {db}.{sch}.EVIDENCE WHERE build_id = %s", [b["id"]]),
                 (f"DELETE FROM {db}.{sch}.BUNDLES WHERE build_id = %s", [b["id"]]),
                 (f"INSERT INTO {db}.{sch}.BUNDLES (build_id, commit_sha, branch, generated_at, catalog_version, records_sha256, bundle) "
                  f"SELECT %s, %s, %s, %s, %s, %s, PARSE_JSON(%s)",
                  [b["id"], b["commit"], b.get("branch"), bundle["generatedAt"], bundle["catalogVersion"],
                   bundle["recordsSha256"], json.dumps(bundle)])]
        insert = f"INSERT INTO {db}.{sch}.EVIDENCE ({', '.join(COLUMNS)}) VALUES ({', '.join(['%s'] * len(COLUMNS))})"
        for r in rows(bundle):
            stmts.append((insert, [r[c] for c in COLUMNS]))
        return stmts

    def publish(self, result: dict, ctx, options: dict) -> dict:
        stmts = self.statements(result["bundle"], options)
        if ctx.dry_run:
            return {"connector": self.id, "dryRun": True, "statements": len(stmts)}
        import snowflake.connector  # optional dependency

        kwargs = {"account": os.environ["SNOWFLAKE_ACCOUNT"], "user": os.environ["SNOWFLAKE_USER"],
                  "warehouse": options.get("warehouse"), "role": options.get("role", "CERT_LOADER")}
        if os.environ.get("SNOWFLAKE_PRIVATE_KEY_PATH"):
            kwargs["private_key_file"] = os.environ["SNOWFLAKE_PRIVATE_KEY_PATH"]
        else:
            kwargs["password"] = os.environ.get("SNOWFLAKE_PASSWORD")
        con = snowflake.connector.connect(**{k: v for k, v in kwargs.items() if v})
        try:
            cur = con.cursor()
            for sql, params in stmts:
                cur.execute(sql, params)
            con.commit()
        finally:
            con.close()
        return {"connector": self.id, "loaded": len(stmts) - 3}
