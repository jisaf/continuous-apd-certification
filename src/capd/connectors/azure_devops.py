"""Sink connector: Azure DevOps. Writes a pipeline run summary and one sticky pull request thread.

Summary: writes summary.md and prints ##vso[task.uploadsummary] so it appears on the run's Extensions tab.
PR thread: needs SYSTEM_ACCESSTOKEN (map $(System.AccessToken) in the pipeline) and the build service
must be allowed to contribute to pull requests. Uses SYSTEM_COLLECTIONURI, SYSTEM_TEAMPROJECT,
BUILD_REPOSITORY_ID and SYSTEM_PULLREQUEST_PULLREQUESTID, which Azure Pipelines sets automatically.
"""

from __future__ import annotations

import os
from pathlib import Path

from ..compare import MARKER
from ._http import secret, session


class AzureDevOpsSink:
    id = "azure-devops"
    config_schema = {"type": "object", "properties": {"summaryPath": {"type": "string"}, "prComment": {"type": "boolean"}}}

    def publish(self, result: dict, ctx, options: dict) -> dict:
        out = {"connector": self.id}
        summary = Path(options.get("summaryPath", "out/summary.md"))
        summary.parent.mkdir(parents=True, exist_ok=True)
        summary.write_text(result["markdown"] + "\n", encoding="utf-8")
        out["summary"] = str(summary)
        if os.environ.get("TF_BUILD"):
            print(f"##vso[task.uploadsummary]{summary.resolve()}")
        pr = os.environ.get("SYSTEM_PULLREQUEST_PULLREQUESTID") or ctx.pull_request
        if not options.get("prComment", True) or not pr:
            return out
        org = os.environ.get("SYSTEM_COLLECTIONURI", options.get("collectionUri", "")).rstrip("/")
        project = os.environ.get("SYSTEM_TEAMPROJECT", options.get("project", ""))
        repo = os.environ.get("BUILD_REPOSITORY_ID", options.get("repositoryId", ""))
        base = f"{org}/{project}/_apis/git/repositories/{repo}/pullRequests/{pr}/threads"
        if ctx.dry_run:
            out.update({"dryRun": True, "threadsUrl": base})
            return out
        s = session(options)
        s.headers.update({"Authorization": f"Bearer {secret(options, 'tokenEnv', 'SYSTEM_ACCESSTOKEN')}"})
        params = {"api-version": "7.1"}
        for t in s.get(base, params=params).json().get("value", []):
            comments = t.get("comments") or []
            if comments and MARKER in (comments[0].get("content") or ""):
                if comments[0].get("content") == result["markdown"]:
                    out["action"] = "unchanged"
                    return out
                r = s.patch(f"{base}/{t['id']}/comments/{comments[0]['id']}", params=params, json={"content": result["markdown"]})
                r.raise_for_status()
                out["action"] = "updated"
                return out
        r = s.post(base, params=params, json={"comments": [{"parentCommentId": 0, "content": result["markdown"], "commentType": 1}],
                                              "status": 1})
        r.raise_for_status()
        out["action"] = "created"
        return out
