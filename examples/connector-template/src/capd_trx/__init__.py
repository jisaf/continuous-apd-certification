"""capd source connector: Visual Studio TRX test results.

Rule keys come from test categories, for example in C#:

    [TestMethod]
    [TestCategory("rule:cms:ee:EE21")]
    public void PendsSnapWithoutHoldingMedicaid() { ... }

A test ID is "<class name>::<test name>", so it stays stable across runs and can be compared with main.
"""

from __future__ import annotations

import xml.etree.ElementTree as ET

from capd.connectors._common import expand, test_records
from capd.tags import Sidecar, parse_tag

NS = {"t": "http://microsoft.com/schemas/VisualStudio/TeamTest/2010"}
OUTCOME = {"Passed": "pass", "Failed": "fail", "Error": "error", "Timeout": "error", "Aborted": "error",
           "NotExecuted": "skipped", "Inconclusive": "skipped"}


class TrxSource:
    id = "trx"
    config_schema = {"type": "object", "properties": {"paths": {"type": "array", "items": {"type": "string"}}}}

    def parse(self, path) -> list[dict]:
        root = ET.parse(path).getroot()
        definitions = {}
        for ut in root.iterfind(".//t:TestDefinitions/t:UnitTest", NS):
            method = ut.find("t:TestMethod", NS)
            cats = [c.get("TestCategory", "") for c in ut.iterfind(".//t:TestCategoryItem", NS)]
            definitions[ut.get("id")] = {
                "className": method.get("className", "") if method is not None else "",
                "keys": [k for k in (parse_tag(c) for c in cats) if k],
            }
        cases = []
        for r in root.iterfind(".//t:Results/t:UnitTestResult", NS):
            d = definitions.get(r.get("testId"), {"className": "", "keys": []})
            name = r.get("testName", "")
            cases.append({
                "testId": f"{d['className']}::{name}" if d["className"] else name,
                "name": name,
                "result": OUTCOME.get(r.get("outcome", ""), "error"),
                "keys": d["keys"],
                "sourceUri": str(path),
                "durationMs": _duration_ms(r.get("duration")),
            })
        return cases

    def collect(self, ctx, options: dict) -> list[dict]:
        sidecar = Sidecar.load(options.get("sidecar"))
        cases = []
        for path in expand(options.get("paths"), options.get("base")):
            cases.extend(self.parse(path))
        # test_records merges reruns, validates rule keys against the catalog, and infers programs.
        return test_records(ctx, cases, sidecar)


def _duration_ms(text: str | None) -> float:
    if not text:
        return 0.0
    h, m, s = text.split(":")
    return (int(h) * 3600 + int(m) * 60 + float(s)) * 1000
