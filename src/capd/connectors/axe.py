"""Source connector: axe-core accessibility results (JSON from @axe-core/cli, @axe-core/playwright, or Pa11y's axe runner).

Produces one 'scan' record per scanned page, tagged to CEF12 (Section 508, WCAG 2.2 AA) by default.
This is a leading indicator: automated tools find only part of WCAG issues.
"""

from __future__ import annotations

import json

from ..evidence import make_record
from ._common import expand

IMPACT = {"minor": 1, "moderate": 2, "serious": 3, "critical": 4}


class AxeSource:
    id = "axe"
    config_schema = {"type": "object", "properties": {
        "paths": {"type": "array", "items": {"type": "string"}},
        "rules": {"type": "array", "items": {"type": "string"}},
        "failAt": {"enum": ["minor", "moderate", "serious", "critical"]}}}

    def collect(self, ctx, options: dict) -> list[dict]:
        keys = options.get("rules") or ["cms:cef:CEF12"]
        fail_at = IMPACT[options.get("failAt", "minor")]
        records = []
        for path in expand(options.get("paths"), options.get("base")):
            doc = json.loads(open(path, encoding="utf-8").read())
            pages = doc if isinstance(doc, list) else [doc]
            for page in pages:
                url = page.get("url", str(path))
                failing = [v for v in page.get("violations", []) if IMPACT.get(v.get("impact") or "minor", 1) >= fail_at]
                records.append(make_record(
                    ctx, rule_ids=keys, kind="scan", result="fail" if failing else "pass", source_uri=str(path),
                    test_id=f"scan::accessibility::{url}", name=f"Accessibility scan ({url})",
                    detail={"tool": "axe-core", "url": url}))
        return records
