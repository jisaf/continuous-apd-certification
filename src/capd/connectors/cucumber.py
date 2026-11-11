"""Source connector: Cucumber JSON reports (Cucumber, SpecFlow, Behave, pytest-bdd --cucumberjson).

Rule keys come from Gherkin tags such as @rule:cms:ee:EE21. Feature-level tags apply to every scenario.
"""

from __future__ import annotations

import json

from ..tags import Sidecar, parse_tag
from ._common import expand, test_records


def _keys(tags) -> list[str]:
    out = []
    for t in tags or []:
        k = parse_tag(t.get("name", "") if isinstance(t, dict) else str(t))
        if k:
            out.append(k)
    return out


def _result(steps) -> str:
    statuses = [((s.get("result") or {}).get("status") or "skipped") for s in steps or []]
    if any(s == "failed" for s in statuses):
        return "fail"
    if statuses and all(s == "passed" for s in statuses):
        return "pass"
    if any(s in ("undefined", "pending", "ambiguous") for s in statuses):
        return "error"
    return "skipped"


class CucumberSource:
    id = "cucumber"
    config_schema = {"type": "object", "properties": {"paths": {"type": "array", "items": {"type": "string"}}}}

    def parse(self, path) -> list[dict]:
        cases = []
        for feature in json.loads(open(path, encoding="utf-8").read()):
            fkeys = _keys(feature.get("tags"))
            uri = feature.get("uri") or feature.get("name", "")
            for el in feature.get("elements", []):
                if el.get("type") == "background":
                    continue
                skeys = _keys(el.get("tags"))
                name = el.get("name") or el.get("id", "")
                dur = sum(((s.get("result") or {}).get("duration") or 0) for s in el.get("steps", [])) / 1e6
                ident = el.get("id") or f"{name}@{el.get('line')}"
                cases.append({
                    "testId": f"{uri}::{ident}",
                    "name": name, "result": _result(el.get("steps")), "keys": fkeys + skeys,
                    "sourceUri": str(path), "durationMs": dur,
                })
        return cases

    def collect(self, ctx, options: dict) -> list[dict]:
        sidecar = Sidecar.load(options.get("sidecar"))
        cases = []
        for path in expand(options.get("paths"), options.get("base")):
            cases.extend(self.parse(path))
        return test_records(ctx, cases, sidecar)
