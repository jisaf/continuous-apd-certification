"""Evidence records and the per-run evidence bundle."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from . import SCHEMA_VERSION, schemas


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def make_record(ctx, *, rule_ids, kind, result, source_uri, test_id=None, name=None, value=None,
                unit=None, attempts=None, duration_ms=None, detail=None) -> dict:
    """Build one evidence record from a RunContext. Programs are inferred from the rule keys."""
    rec = {
        "schemaVersion": SCHEMA_VERSION,
        "ruleIds": sorted(set(rule_ids)),
        "kind": kind,
        "result": result,
        "programs": ctx.catalog.programs_for(rule_ids) if ctx.catalog else [],
        "environment": ctx.environment,
        "executedBy": ctx.executed_by,
        "build": ctx.build_id,
        "commit": ctx.commit,
        "observedAt": ctx.observed_at,
        "sourceUri": source_uri,
    }
    for k, v in (("testId", test_id), ("name", name), ("value", value), ("unit", unit),
                 ("attempts", attempts), ("durationMs", duration_ms), ("detail", detail)):
        if v is not None:
            rec[k] = v
    return rec


def _sha(obj) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def build_bundle(ctx, records: list[dict], warnings: list[str] | None = None) -> dict:
    records = sorted(records, key=lambda r: (r.get("testId") or "", r["kind"], r["sourceUri"], ",".join(r["ruleIds"])))
    bundle = {
        "schemaVersion": SCHEMA_VERSION,
        "catalogVersion": ctx.catalog.version if ctx.catalog else "unknown",
        "generatedAt": ctx.observed_at,
        "build": {k: v for k, v in {
            "id": ctx.build_id, "commit": ctx.commit, "branch": ctx.branch,
            "pipeline": ctx.pipeline, "url": ctx.build_url, "pullRequest": ctx.pull_request}.items() if v},
        "environment": ctx.environment,
        "records": records,
        "warnings": warnings or [],
        "recordsSha256": _sha(records),
    }
    schemas.check("evidence-bundle", bundle)
    return bundle


def save(bundle: dict, path: str | Path) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(bundle, indent=1) + "\n", encoding="utf-8")


def load(path: str | Path) -> dict:
    bundle = json.loads(Path(path).read_text(encoding="utf-8"))
    schemas.check("evidence-bundle", bundle)
    if _sha(bundle["records"]) != bundle["recordsSha256"]:
        raise ValueError(f"{path}: recordsSha256 does not match the records (the bundle was changed)")
    return bundle


def test_results(bundle: dict) -> dict[str, dict]:
    """Map testId -> record for test-kind records."""
    return {r["testId"]: r for r in bundle["records"] if r["kind"] == "test" and r.get("testId")}
