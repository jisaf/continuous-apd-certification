"""Sink connector: Jira. One issue per gate with a checklist summary, plus one issue per regression
(a blocker) that closes itself when the test passes again. Issues go to a separate certification
project by default so they never clutter sprint boards.

Needs JIRA_EMAIL and JIRA_API_TOKEN (Jira Cloud) or JIRA_TOKEN (Data Center bearer token).
Options: baseUrl, project (default CERT), issueType (default Task), doneTransition (default "Done").
"""

from __future__ import annotations

import os

from ._http import session

GATES = {"ORR": "CMS Operational Readiness Review", "FNA-UAT": "FNA UAT Go/No-Go"}


def _label(text: str) -> str:
    return "capd-" + "".join(ch if ch.isalnum() else "-" for ch in text).strip("-").lower()[:80]


class JiraSink:
    id = "jira"
    config_schema = {"type": "object", "required": ["baseUrl"], "properties": {
        "baseUrl": {"type": "string"}, "project": {"type": "string"}, "issueType": {"type": "string"},
        "doneTransition": {"type": "string"}}}

    def plan(self, result: dict) -> list[dict]:
        cmp = result.get("comparison") or {"regressions": [], "fixed": []}
        bundle = result["bundle"]
        tagged = [r for r in bundle["records"] if r["kind"] == "test" and r["ruleIds"]]
        actions = []
        for gate, title in GATES.items():
            prefix = ("cms:",) if gate == "ORR" else ("fna:",)
            rel = [r for r in tagged if any(k.startswith(prefix) for k in r["ruleIds"])]
            ok = sum(1 for r in rel if r["result"] == "pass")
            desc = (f"Build {bundle['build']['id']}: {ok} of {len(rel)} tagged tests passing for {title}. "
                    f"Open regressions: {len(cmp['regressions'])}. Readiness signal only; rule status is in the report layer.")
            actions.append({"op": "upsert", "label": _label("gate-" + gate), "summary": f"Certification gate: {title}", "description": desc})
        for r in cmp["regressions"]:
            actions.append({"op": "upsert", "label": _label("blocker-" + r["testId"]),
                            "summary": f"Certification regression: {r['name']}"[:250],
                            "description": f"Rules: {', '.join(r['ruleIds'])}. Was {r['was']} on main, now {r['now']}."})
        for r in cmp["fixed"]:
            actions.append({"op": "close", "label": _label("blocker-" + r["testId"])})
        return actions

    def publish(self, result: dict, ctx, options: dict) -> dict:
        actions = self.plan(result)
        if ctx.dry_run:
            return {"connector": self.id, "dryRun": True, "actions": actions}
        base = options["baseUrl"].rstrip("/")
        project = options.get("project", "CERT")
        s = session(options)
        if os.environ.get("JIRA_API_TOKEN"):
            s.auth = (os.environ.get("JIRA_EMAIL", ""), os.environ["JIRA_API_TOKEN"])
        elif os.environ.get("JIRA_TOKEN"):
            s.headers.update({"Authorization": f"Bearer {os.environ['JIRA_TOKEN']}"})
        done = []
        for a in actions:
            found = s.get(f"{base}/rest/api/2/search", params={"jql": f'project = "{project}" AND labels = "{a["label"]}"',
                                                                "fields": "status", "maxResults": 1}).json().get("issues", [])
            if a["op"] == "upsert":
                if found:
                    s.put(f"{base}/rest/api/2/issue/{found[0]['key']}",
                          json={"fields": {"description": a["description"]}}).raise_for_status()
                    done.append({"updated": found[0]["key"]})
                else:
                    r = s.post(f"{base}/rest/api/2/issue", json={"fields": {
                        "project": {"key": project}, "summary": a["summary"], "description": a["description"],
                        "issuetype": {"name": options.get("issueType", "Task")}, "labels": ["capd", a["label"]]}})
                    r.raise_for_status()
                    done.append({"created": r.json().get("key")})
            elif a["op"] == "close" and found:
                key = found[0]["key"]
                trans = s.get(f"{base}/rest/api/2/issue/{key}/transitions").json().get("transitions", [])
                t = next((t for t in trans if t["name"].lower() == options.get("doneTransition", "Done").lower()), None)
                if t:
                    s.post(f"{base}/rest/api/2/issue/{key}/transitions", json={"transition": {"id": t["id"]}}).raise_for_status()
                    done.append({"closed": key})
        return {"connector": self.id, "results": done}
