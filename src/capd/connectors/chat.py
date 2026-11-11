"""Sink connector: chat digest to a Slack or Microsoft Teams incoming webhook.

Posts only when the readiness summary changed since the last post (state is kept in a small file),
so the channel hears about changes, not every build. Set the webhook URL in CAPD_CHAT_WEBHOOK.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from ._http import secret, session


class ChatDigestSink:
    id = "chat"
    config_schema = {"type": "object", "properties": {"stateFile": {"type": "string"}, "format": {"enum": ["slack", "teams"]},
                                                      "webhookEnv": {"type": "string"}}}

    def message(self, result: dict) -> str:
        c = result.get("comparison") or {}
        reg = len(c.get("regressions", []))
        line = (f"Certification readiness, build {result['bundle']['build']['id']}: "
                f"{c.get('taggedPassing', '?')} of {c.get('taggedTests', '?')} tagged tests passing; "
                f"{reg} regression{'s' if reg != 1 else ''} vs main.")
        if result.get("reportUrl"):
            line += f" Report: {result['reportUrl']}"
        return line

    def publish(self, result: dict, ctx, options: dict) -> dict:
        c = result.get("comparison") or {}
        state = {"regressions": sorted(r["testId"] for r in c.get("regressions", [])),
                 "failing": c.get("taggedTests", 0) - c.get("taggedPassing", 0)}
        digest = hashlib.sha256(json.dumps(state, sort_keys=True).encode()).hexdigest()
        sf = Path(options.get("stateFile", "out/chat-state.json"))
        previous = json.loads(sf.read_text()).get("digest") if sf.exists() else None
        if previous == digest:
            return {"connector": self.id, "action": "unchanged"}
        text = self.message(result)
        payload = {"text": text}
        if ctx.dry_run:
            return {"connector": self.id, "dryRun": True, "payload": payload}
        url = secret(options, "webhookEnv", "CAPD_CHAT_WEBHOOK")
        if not url:
            return {"connector": self.id, "skipped": "no webhook configured"}
        session(options).post(url, json=payload).raise_for_status()
        sf.parent.mkdir(parents=True, exist_ok=True)
        sf.write_text(json.dumps({"digest": digest}))
        return {"connector": self.id, "action": "posted"}
