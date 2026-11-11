"""Sink connector: write the bundle and comparison to a folder, plus newline-delimited JSON rows
that any SQL data platform can load (one row per evidence record, one per rule key)."""

from __future__ import annotations

import json
from pathlib import Path


def rows(bundle: dict) -> list[dict]:
    """Flatten a bundle into one row per (record, rule key) for the report layer's EVIDENCE table."""
    b = bundle["build"]
    out = []
    for r in bundle["records"]:
        for key in r["ruleIds"] or [None]:
            out.append({
                "build_id": b["id"], "commit_sha": b["commit"], "branch": b.get("branch"),
                "generated_at": bundle["generatedAt"], "catalog_version": bundle["catalogVersion"],
                "rule_key": key, "kind": r["kind"], "result": r["result"], "value": r.get("value"),
                "unit": r.get("unit"), "programs": ",".join(r.get("programs", [])), "environment": r["environment"],
                "executed_by": r["executedBy"], "test_id": r.get("testId"), "name": r.get("name"),
                "observed_at": r["observedAt"], "source_uri": r["sourceUri"],
            })
    return out


class FileSink:
    id = "file"
    config_schema = {"type": "object", "properties": {"dir": {"type": "string"}}}

    def publish(self, result: dict, ctx, options: dict) -> dict:
        d = Path(options.get("dir", "out"))
        d.mkdir(parents=True, exist_ok=True)
        (d / "evidence-rows.ndjson").write_text("".join(json.dumps(r) + "\n" for r in rows(result["bundle"])), encoding="utf-8")
        if result.get("comparison"):
            (d / "comparison.json").write_text(json.dumps(result["comparison"], indent=1) + "\n", encoding="utf-8")
        if result.get("markdown"):
            (d / "summary.md").write_text(result["markdown"] + "\n", encoding="utf-8")
        return {"connector": self.id, "dir": str(d)}
