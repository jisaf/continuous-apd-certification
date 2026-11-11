"""Source connector: Playwright JSON reports (npx playwright test --reporter=json).

Rule keys come from Playwright tags, for example:

    test('pends SNAP without holding Medicaid', { tag: '@rule:cms:ee:EE21' }, async ({ page }) => { ... });

Tags in the test title (... @rule:cms:ee:EE21) and on describe blocks also work. A test ID is
"<file>::<describe path> › <title>", so it stays stable across runs. Retries are merged: a test that
passed on any attempt counts as passing.
"""

from __future__ import annotations

import json
import re

from ..tags import Sidecar, parse_tag
from ._common import expand, test_records

STATUS = {"passed": "pass", "failed": "fail", "timedOut": "fail", "interrupted": "error", "skipped": "skipped"}
TITLE_TAG = re.compile(r"@rule:\S+")


def _keys(tags, title: str) -> list[str]:
    found = [parse_tag(t) for t in (tags or [])] + [parse_tag(m) for m in TITLE_TAG.findall(title or "")]
    return [k for k in found if k]


class PlaywrightSource:
    id = "playwright"
    config_schema = {"type": "object", "properties": {"paths": {"type": "array", "items": {"type": "string"}}}}

    def parse(self, path) -> list[dict]:
        cases: list[dict] = []

        def walk(suite, parents: list[str], inherited: list[str]):
            title = suite.get("title", "")
            clean = TITLE_TAG.sub("", title).strip()   # tags never change a test's identity
            here = parents + ([clean] if clean and not clean.endswith((".ts", ".js", ".mjs", ".cjs")) else [])
            keys_here = inherited + _keys(None, title)
            for spec in suite.get("specs", []):
                spec_keys = keys_here + _keys(spec.get("tags"), spec.get("title", ""))
                for test in spec.get("tests", []):
                    results = test.get("results") or [{"status": "skipped"}]
                    clean_title = TITLE_TAG.sub("", spec.get("title", "")).strip()
                    tid = f"{spec.get('file') or suite.get('file', '')}::{' › '.join(here + [clean_title])}"
                    if test.get("projectName"):
                        tid += f" [{test['projectName']}]"
                    for r in results:
                        cases.append({"testId": tid, "name": clean_title, "result": STATUS.get(r.get("status"), "error"),
                                      "keys": spec_keys + _keys(test.get("tags"), ""), "sourceUri": str(path),
                                      "durationMs": r.get("duration") or 0})
            for child in suite.get("suites", []):
                walk(child, here, keys_here)

        report = json.loads(open(path, encoding="utf-8").read())
        for suite in report.get("suites", []):
            walk(suite, [], [])
        return cases

    def collect(self, ctx, options: dict) -> list[dict]:
        sidecar = Sidecar.load(options.get("sidecar"))
        cases = []
        for path in expand(options.get("paths"), options.get("base")):
            cases.extend(self.parse(path))
        return test_records(ctx, cases, sidecar)
