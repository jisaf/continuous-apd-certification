"""The pull request gate: compare this run's tagged results with the last build on main.

A regression is a tagged test or scan that passed on main and now fails or errors.
Only regressions can block, and only when gateMode is 'blocking'; quarantined tests never block.
"""

from __future__ import annotations

from pathlib import Path

MARKER = "<!-- capd-certification-report -->"
BAD = ("fail", "error")


def load_quarantine(path: str | Path | None) -> set[str]:
    if not path or not Path(path).exists():
        return set()
    lines = Path(path).read_text(encoding="utf-8").splitlines()
    return {ln.split("#", 1)[0].strip() for ln in lines if ln.split("#", 1)[0].strip()}


def _tracked(bundle: dict) -> dict[str, dict]:
    return {r["testId"]: r for r in bundle["records"]
            if r.get("testId") and r["kind"] in ("test", "scan") and r["ruleIds"]}


def compare(current: dict, baseline: dict | None, quarantine: set[str] | None = None, mode: str = "report-only") -> dict:
    quarantine = quarantine or set()
    cur = _tracked(current)
    base = _tracked(baseline) if baseline else {}
    regressions, fixed, new_failures, quarantined = [], [], [], []

    def item(tid, was, now):
        r = cur.get(tid) or base.get(tid)
        return {"testId": tid, "name": r.get("name") or tid, "ruleIds": r["ruleIds"], "was": was, "now": now}

    for tid, r in sorted(cur.items()):
        was = base.get(tid, {}).get("result")
        if r["result"] in BAD:
            if tid in quarantine:
                quarantined.append(item(tid, was, r["result"]))
            elif was == "pass":
                regressions.append(item(tid, was, r["result"]))
            elif was is None:
                new_failures.append(item(tid, was, r["result"]))
        elif r["result"] == "pass" and was in BAD:
            fixed.append(item(tid, was, "pass"))

    tests = [r for r in cur.values() if r["kind"] == "test"]
    rules = sorted({k for r in cur.values() for k in r["ruleIds"]})
    return {
        "mode": mode,
        "baselineBuild": (baseline or {}).get("build", {}).get("id"),
        "currentBuild": current["build"]["id"],
        "regressions": regressions,
        "fixed": fixed,
        "newFailures": new_failures,
        "quarantined": quarantined,
        "taggedTests": len(tests),
        "taggedPassing": sum(1 for r in tests if r["result"] == "pass"),
        "rulesWithEvidence": len(rules),
        "blocking": mode == "blocking" and bool(regressions),
    }


def markdown(result: dict, report_url: str | None = None) -> str:
    lines = [MARKER, "### Certification readiness check"]
    n = len(result["regressions"])
    if n:
        verdict = "blocks this change" if result["blocking"] else "reported only (gate is in report-only mode)"
        lines.append(f"**{n} certification regression{'s' if n != 1 else ''}**: {verdict}.")
    else:
        lines.append("**No certification regressions** compared with main.")
    lines.append("")
    lines.append(f"Tagged tests passing: {result['taggedPassing']} of {result['taggedTests']} · "
                 f"rules with evidence: {result['rulesWithEvidence']} · baseline build: {result['baselineBuild'] or 'none'}")
    for title, key in (("Regressions", "regressions"), ("New failing tagged tests", "newFailures"),
                       ("Fixed", "fixed"), ("Quarantined (not blocking)", "quarantined")):
        rows = result[key]
        if rows:
            lines += ["", f"**{title}**", "", "| Test | Rules | Main | This run |", "| --- | --- | --- | --- |"]
            for r in rows[:30]:
                lines.append(f"| {r['name']} | {', '.join(r['ruleIds'])} | {r['was'] or '—'} | {r['now']} |")
            if len(rows) > 30:
                lines.append(f"| … {len(rows) - 30} more | | | |")
    if report_url:
        lines += ["", f"[Open the full static report]({report_url})"]
    lines += ["", "<sub>Readiness signal only. Rule status (Met) and agency findings are decided in the report layer and by CMS and FNA.</sub>"]
    return "\n".join(lines)
