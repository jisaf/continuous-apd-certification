"""Static HTML report: one self-contained file per build, built from the pipeline's evidence bundle alone.

It never reads external data (Jira, production data, security findings, documents). Scans appear as
pass or fail only, because the reports repository may be public. Rule status such as Met is decided
in the report layer, not here.
"""

from __future__ import annotations

from collections import defaultdict
from html import escape

GATE_SETS = [
    ("CMS Operational Readiness Review (ORR)", "ORR", ["cms:ee", "cms:cef"]),
    ("FNA UAT and pilot Go/No-Go", "FNA-UAT", ["fna:sirt", "fna:golive"]),
]
SET_NAMES = {"cms:ee": "CMS E&E outcomes", "cms:cef": "CMS Conditions for Enhanced Funding",
             "fna:sirt": "SNAP System Integrity Review Tool (SIRT)", "fna:golive": "SNAP Go Live Requirements"}

CSS = """
:root{--ink:#1b1b1b;--muted:#565c65;--line:#dfe1e2;--ok:#00703c;--bad:#b50909;--warn:#8a5300;--bg:#f7f8f9;--accent:#1a4480}
*{box-sizing:border-box}body{margin:0;font:16px/1.5 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;color:var(--ink);background:#fff}
main{max-width:1100px;margin:0 auto;padding:24px}h1{font-size:1.6rem;margin:0 0 4px}h2{font-size:1.25rem;margin:32px 0 8px;border-bottom:1px solid var(--line);padding-bottom:4px}
h3{font-size:1.05rem;margin:20px 0 6px}.meta{color:var(--muted);font-size:.9rem}.note{background:var(--bg);border-left:4px solid var(--accent);padding:10px 14px;margin:16px 0}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px;margin:16px 0}.tile{border:1px solid var(--line);border-radius:8px;padding:12px}
.tile .n{font-size:1.6rem;font-weight:700}.tile .l{color:var(--muted);font-size:.9rem}
table{border-collapse:collapse;width:100%;margin:8px 0 16px;font-size:.92rem}th,td{border-bottom:1px solid var(--line);padding:6px 8px;text-align:left;vertical-align:top}
th{background:var(--bg)}code{font-size:.85em}.pass{color:var(--ok);font-weight:600}.fail,.error{color:var(--bad);font-weight:600}.skipped{color:var(--muted)}
.warn{color:var(--warn)}details{margin:6px 0}summary{cursor:pointer;font-weight:600}footer{color:var(--muted);font-size:.85rem;margin-top:40px}
.bar{height:8px;background:var(--line);border-radius:4px;overflow:hidden}.bar span{display:block;height:100%;background:var(--accent)}
"""


def _result(r: str) -> str:
    label = {"pass": "Pass", "fail": "Fail", "error": "Error", "skipped": "Skipped"}.get(r, r)
    return f'<span class="{escape(r)}">{label}</span>'


def _short(catalog, key: str) -> str:
    rule = catalog.get(key) if catalog else None
    return f"{key} ({rule['sourceId']})" if rule and rule["sourceId"] not in key else key


def _rule_label(catalog, key: str) -> str:
    rule = catalog.get(key) if catalog else None
    title = rule["title"] if rule else "(not in catalog)"
    src = f"{rule['sourceId']} · " if rule else ""
    return f"<code>{escape(key)}</code><br><span class=meta>{escape(src + title)}</span>"


def render(bundle: dict, catalog, comparison: dict | None = None, title: str = "Certification readiness report") -> str:
    recs = bundle["records"]
    tests = [r for r in recs if r["kind"] == "test"]
    tagged = [r for r in tests if r["ruleIds"]]
    scans = [r for r in recs if r["kind"] == "scan"]
    by_rule: dict[str, list[dict]] = defaultdict(list)
    for r in tagged:
        for k in r["ruleIds"]:
            by_rule[k].append(r)
    b = bundle["build"]
    out = [f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
           f"<title>{escape(title)}</title><style>{CSS}</style></head><body><main>"]
    out.append(f"<h1>{escape(title)}</h1>")
    out.append(f'<p class="meta">Build <strong>{escape(b["id"])}</strong> · commit <code>{escape(b["commit"][:12])}</code>'
               f'{" · branch " + escape(b["branch"]) if b.get("branch") else ""} · generated {escape(bundle["generatedAt"])}'
               f' · catalog {escape(bundle["catalogVersion"])} · environment {escape(bundle.get("environment", ""))}</p>')
    out.append('<div class="note"><strong>What this report shows.</strong> Only data this pipeline run produced: tagged test '
               "results, scans (pass or fail), and checks on rule tags. It does not decide whether a rule is Met, and it is "
               "not a CMS or FNA finding. Rule status, state acceptance, production metrics, and documents live in the "
               "state's report layer.</div>")

    passing = sum(1 for r in tagged if r["result"] == "pass")
    failing = sum(1 for r in tagged if r["result"] in ("fail", "error"))
    regress = len(comparison["regressions"]) if comparison else None
    tiles = [
        (f"{passing} / {len(tagged)}", "tagged tests passing"),
        (str(failing), "tagged tests failing"),
        ("—" if regress is None else str(regress), "regressions vs main" + ("" if comparison and comparison.get("baselineBuild") else " (no baseline)")),
        (str(len(by_rule)), "rules with test evidence"),
        (f"{sum(1 for s in scans if s['result'] == 'pass')} / {len(scans)}", "scans passing"),
        (str(len(bundle.get("warnings", []))), "tag warnings"),
    ]
    out.append('<section aria-label="Summary"><div class="tiles">' + "".join(
        f'<div class="tile"><div class="n">{escape(n)}</div><div class="l">{escape(lbl)}</div></div>' for n, lbl in tiles) + "</div></section>")

    if comparison:
        out.append("<h2>Compared with main</h2>")
        mode = "blocking" if comparison["mode"] == "blocking" else "report-only"
        out.append(f'<p>Gate mode: <strong>{mode}</strong>. Baseline build: {escape(str(comparison.get("baselineBuild") or "none"))}.</p>')
        for heading, key in (("Regressions", "regressions"), ("New failing tagged tests", "newFailures"),
                             ("Fixed since main", "fixed"), ("Quarantined (do not block)", "quarantined")):
            rows = comparison[key]
            if not rows:
                continue
            out.append(f"<h3>{heading} ({len(rows)})</h3><table><thead><tr><th scope=col>Test</th><th scope=col>Rules</th>"
                       "<th scope=col>Main</th><th scope=col>This run</th></tr></thead><tbody>")
            for r in rows:
                out.append(f"<tr><td>{escape(r['name'])}</td><td>{escape(', '.join(_short(catalog, k) for k in r['ruleIds']))}</td>"
                           f"<td>{_result(r['was']) if r['was'] else '—'}</td><td>{_result(r['now'])}</td></tr>")
            out.append("</tbody></table>")
        if not any(comparison[k] for k in ("regressions", "newFailures", "fixed", "quarantined")):
            out.append("<p>No changes in tagged results since main.</p>")

    out.append("<h2>Test evidence by gate</h2>")
    out.append("<p>For each rule set: how many rules that call for automated tests already have at least one tagged test, "
               "and the latest result of each tagged rule. Rules that rest on documents, attestations, or demonstrations are "
               "tracked in the report layer, not here.</p>")
    for heading, gate, sets in GATE_SETS:
        out.append(f"<h3>{escape(heading)}</h3>")
        for s in sets:
            agency, rset = s.split(":")
            wanted = [r for r in (catalog.rules.values() if catalog else [])
                      if r["agency"] == agency and r["set"] == rset and "test" in r["gates"].get(gate, []) and r.get("applicable", True)]
            covered = [r for r in wanted if r["key"] in by_rule]
            pct = (100 * len(covered) // len(wanted)) if wanted else 0
            out.append(f"<p><strong>{escape(SET_NAMES[s])}</strong>: {len(covered)} of {len(wanted)} test-evidenced rules have tagged tests."
                       f'<span class="bar" role="img" aria-label="{pct} percent"><span style="width:{pct}%"></span></span></p>')
            keys = sorted(k for k in by_rule if k.startswith(s + ":"))
            if keys:
                out.append(f"<details><summary>Tagged rules ({len(keys)})</summary><table><thead><tr><th scope=col>Rule</th>"
                           "<th scope=col>Tests passing</th><th scope=col>Latest result</th></tr></thead><tbody>")
                for k in keys:
                    rs = by_rule[k]
                    ok = sum(1 for r in rs if r["result"] == "pass")
                    worst = "fail" if any(r["result"] in ("fail", "error") for r in rs) else ("pass" if ok else "skipped")
                    out.append(f"<tr><td>{_rule_label(catalog, k)}</td><td>{ok} of {len(rs)}</td><td>{_result(worst)}</td></tr>")
                out.append("</tbody></table></details>")
            missing = [r for r in wanted if r["key"] not in by_rule]
            if missing:
                out.append(f"<details><summary>Test-evidenced rules with no tagged test yet ({len(missing)})</summary><ul>")
                for r in missing[:400]:
                    out.append(f"<li><code>{escape(r['key'])}</code> {escape(r['sourceId'])}: {escape(r['title'])}</li>")
                if len(missing) > 400:
                    out.append(f"<li>… {len(missing) - 400} more</li>")
                out.append("</ul></details>")

    out.append("<h2>Scans</h2>")
    if scans:
        out.append("<table><thead><tr><th scope=col>Scan</th><th scope=col>Rules</th><th scope=col>Result</th></tr></thead><tbody>")
        for s in scans:
            out.append(f"<tr><td>{escape(s.get('name') or s['testId'])}</td><td>{escape(', '.join(_short(catalog, k) for k in s['ruleIds']))}</td><td>{_result(s['result'])}</td></tr>")
        out.append("</tbody></table><p class=meta>Pass or fail only. Counts and details stay in the report layer.</p>")
    else:
        out.append("<p>No scans in this run.</p>")

    out.append("<h2>Tag checks</h2>")
    warns = bundle.get("warnings", [])
    untagged = [r for r in tests if not r["ruleIds"]]
    out.append(f"<p>{len(tagged)} tagged tests, {len(untagged)} untagged tests.</p>")
    if warns:
        out.append('<ul class="warn">' + "".join(f"<li>{escape(w)}</li>" for w in warns[:200]) + "</ul>")
    else:
        out.append("<p>No tag warnings.</p>")

    out.append('<footer>Generated by capd, the continuous APD certification toolkit (Apache-2.0). Rules from the CMS MES '
               "Certification Repository, the SNAP System Integrity Review Tool, and the SNAP Eligibility System Go Live "
               "Requirements. Readiness signal only.</footer></main></body></html>")
    return "".join(out)
