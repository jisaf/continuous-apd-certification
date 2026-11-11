"""check-tags: lint rule tags so they stay correct as tests change."""

from __future__ import annotations

import fnmatch

from .catalog import is_key


def check(bundle: dict, catalog, tagged_paths: list[str] | None = None) -> list[str]:
    issues = []
    for w in bundle.get("warnings", []):
        if w.startswith("unknown rule key"):
            issues.append(w)
    for r in bundle["records"]:
        for k in r["ruleIds"]:
            if not is_key(k):
                issues.append(f"malformed rule key '{k}' on {r.get('testId') or r['sourceUri']}")
            elif catalog is not None and k not in catalog:
                issues.append(f"rule key '{k}' is not in catalog {catalog.version} (test {r.get('testId')})")
            elif catalog is not None and not catalog.applicable(k):
                issues.append(f"rule key '{k}' is marked not applicable in this state's configuration (test {r.get('testId')})")
        if r["kind"] == "test" and not r["ruleIds"] and tagged_paths:
            tid = r.get("testId", "")
            if any(fnmatch.fnmatchcase(tid, p) for p in tagged_paths):
                issues.append(f"untagged test in a tagged path: {tid}")
    return sorted(set(issues))
