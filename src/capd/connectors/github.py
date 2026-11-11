"""Sink connector: one sticky pull request comment on GitHub, updated in place, only when it changes.

Needs GITHUB_TOKEN (or the variable named by options.tokenEnv) with pull-requests: write.
Options: repository ("owner/name"; defaults to GITHUB_REPOSITORY), pullRequest (number; defaults to ctx.pull_request).
"""

from __future__ import annotations

import os

from ..compare import MARKER
from ._http import secret, session

API = "https://api.github.com"


class GitHubSink:
    id = "github"
    config_schema = {"type": "object", "properties": {"repository": {"type": "string"}, "pullRequest": {"type": "string"},
                                                      "tokenEnv": {"type": "string"}, "apiUrl": {"type": "string"}}}

    def publish(self, result: dict, ctx, options: dict) -> dict:
        repo = options.get("repository") or os.environ.get("GITHUB_REPOSITORY")
        pr = str(options.get("pullRequest") or ctx.pull_request or "")
        body = result["markdown"]
        if not repo or not pr:
            return {"connector": self.id, "skipped": "not a pull request build"}
        if ctx.dry_run:
            return {"connector": self.id, "dryRun": True, "repository": repo, "pullRequest": pr, "body": body}
        api = options.get("apiUrl", API)
        s = session(options)
        s.headers.update({"Authorization": f"Bearer {secret(options, 'tokenEnv', 'GITHUB_TOKEN')}",
                          "Accept": "application/vnd.github+json"})
        existing = None
        for c in s.get(f"{api}/repos/{repo}/issues/{pr}/comments", params={"per_page": 100}).json():
            if MARKER in (c.get("body") or ""):
                existing = c
                break
        if existing and existing.get("body") == body:
            return {"connector": self.id, "action": "unchanged", "commentId": existing["id"]}
        if existing:
            r = s.patch(f"{api}/repos/{repo}/issues/comments/{existing['id']}", json={"body": body})
            action = "updated"
        else:
            r = s.post(f"{api}/repos/{repo}/issues/{pr}/comments", json={"body": body})
            action = "created"
        r.raise_for_status()
        return {"connector": self.id, "action": action, "commentId": r.json().get("id")}
