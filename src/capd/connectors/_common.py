"""Shared helpers for source connectors."""

from __future__ import annotations

import glob
from pathlib import Path

from ..catalog import is_key
from ..evidence import make_record
from ..tags import Sidecar

RANK = {"pass": 3, "error": 2, "fail": 1, "skipped": 0}


def expand(paths, base: str | None = None) -> list[Path]:
    out: list[Path] = []
    for p in paths or []:
        pattern = str(Path(base) / p) if base and not Path(p).is_absolute() else str(p)
        out.extend(Path(x) for x in sorted(glob.glob(pattern, recursive=True)))
    return out


def merge_attempts(results: list[str]) -> str:
    """A test counts as passing if any attempt passed (a failed test is rerun once in CI)."""
    if "pass" in results:
        return "pass"
    if "error" in results:
        return "error"
    if "fail" in results:
        return "fail"
    return "skipped"


def test_records(ctx, cases: list[dict], sidecar: Sidecar) -> list[dict]:
    """cases: dicts with testId, name, result, keys, sourceUri, durationMs. Merges reruns of the same testId."""
    grouped: dict[str, dict] = {}
    for c in cases:
        g = grouped.setdefault(c["testId"], {**c, "results": [], "keys": set(), "durationMs": 0.0})
        g["results"].append(c["result"])
        g["keys"].update(c.get("keys", []))
        g["durationMs"] += c.get("durationMs") or 0.0
    records = []
    for tid, g in grouped.items():
        keys = set(g["keys"]) | set(sidecar.keys_for(tid))
        bad = sorted(k for k in keys if not is_key(k) or (ctx.catalog and k not in ctx.catalog))
        for k in bad:
            ctx.warn(f"unknown rule key '{k}' on test {tid}")
        keys = sorted(k for k in keys if k not in bad)
        records.append(make_record(
            ctx, rule_ids=keys, kind="test", result=merge_attempts(g["results"]), source_uri=g["sourceUri"],
            test_id=tid, name=g.get("name"), attempts=len(g["results"]), duration_ms=round(g["durationMs"], 1)))
    return records
