"""Source connector: JUnit XML test reports (pytest, JUnit 5, Jest, Azure DevOps test tasks, and others).

Rule keys come from <property name="rule" value="cms:ee:EE21"/> on a <testcase> (or its <testsuite>),
or from a sidecar file. The capd pytest plugin writes these properties from @pytest.mark.rule(...).
"""

from __future__ import annotations

import fnmatch
import xml.etree.ElementTree as ET

from ..tags import Sidecar, parse_tag, split_values
from ._common import expand, test_records


def _props(el) -> list[str]:
    keys = []
    props = el.find("properties")
    if props is not None:
        for p in props.findall("property"):
            if p.get("name") in ("rule", "rules", "tag", "tags"):
                for v in split_values(p.get("value", "")):
                    keys.append(parse_tag(v) or v.lstrip("@"))
    return keys


class JUnitSource:
    id = "junit"
    config_schema = {"type": "object", "properties": {
        "paths": {"type": "array", "items": {"type": "string"}},
        "exclude": {"type": "array", "items": {"type": "string"}, "description": "test ID patterns to skip (for example tests reported by another source)"}}}

    def parse(self, path) -> list[dict]:
        root = ET.parse(path).getroot()
        suites = [root] if root.tag == "testsuite" else root.iter("testsuite")
        cases = []
        for suite in suites:
            suite_keys = _props(suite)
            for tc in suite.findall("testcase"):
                classname, name = tc.get("classname", ""), tc.get("name", "")
                if tc.find("failure") is not None:
                    result = "fail"
                elif tc.find("error") is not None:
                    result = "error"
                elif tc.find("skipped") is not None:
                    result = "skipped"
                else:
                    result = "pass"
                cases.append({
                    "testId": f"{classname}::{name}" if classname else name,
                    "name": name, "result": result, "keys": suite_keys + _props(tc),
                    "sourceUri": str(path), "durationMs": float(tc.get("time") or 0) * 1000,
                })
        return cases

    def collect(self, ctx, options: dict) -> list[dict]:
        sidecar = Sidecar.load(options.get("sidecar"))
        cases = []
        for path in expand(options.get("paths"), options.get("base")):
            cases.extend(c for c in self.parse(path)
                         if not any(fnmatch.fnmatchcase(c["testId"], p) for p in options.get("exclude", [])))
        return test_records(ctx, cases, sidecar)
