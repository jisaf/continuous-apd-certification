"""Source connector: SARIF security scan results (CodeQL, Semgrep, ruff, Trivy, OWASP ZAP via converters).

Produces one 'scan' record per scanned tool: pass when no finding at or above the failing severity.
Counts stay out of the bundle unless includeCounts is set, because static reports may be public;
the report layer is the place for counts and details.
"""

from __future__ import annotations

import json

from ..evidence import make_record
from ._common import expand

LEVELS = {"none": 0, "note": 1, "warning": 2, "error": 3}


class SarifSource:
    id = "sarif"
    config_schema = {"type": "object", "properties": {
        "paths": {"type": "array", "items": {"type": "string"}},
        "rules": {"type": "array", "items": {"type": "string"}},
        "failAt": {"enum": ["note", "warning", "error"]},
        "includeCounts": {"type": "boolean"}}}

    def collect(self, ctx, options: dict) -> list[dict]:
        keys = options.get("rules") or ["cms:cef:CEF09"]
        fail_at = LEVELS[options.get("failAt", "warning")]
        records = []
        for path in expand(options.get("paths"), options.get("base")):
            doc = json.loads(open(path, encoding="utf-8").read())
            for run in doc.get("runs", []):
                tool = ((run.get("tool") or {}).get("driver") or {}).get("name", "scanner")
                levels = [LEVELS.get(r.get("level", "warning"), 2) for r in run.get("results", [])]
                failing = sum(1 for lv in levels if lv >= fail_at)
                detail = {"tool": tool}
                if options.get("includeCounts"):
                    detail.update({"findings": len(levels), "failing": failing})
                records.append(make_record(
                    ctx, rule_ids=keys, kind="scan", result="fail" if failing else "pass",
                    source_uri=str(path), test_id=f"scan::security::{tool}", name=f"Security scan ({tool})", detail=detail))
        return records
