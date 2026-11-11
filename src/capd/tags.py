"""Rule-key tags: how tests name the rules they prove.

Accepted forms (the same key syntax everywhere):
  Gherkin / Cucumber:   @rule:cms:ee:EE21
  pytest:               @pytest.mark.rule("cms:ee:EE21")  -> JUnit XML <property name="rule" value="cms:ee:EE21"/>
  JUnit 5 / others:     <property name="rule" value="..."/> (comma or space separated values allowed)
  Sidecar file:         a YAML map of test-ID glob patterns to rule keys, for frameworks that cannot carry tags
"""

from __future__ import annotations

import fnmatch
import re
from pathlib import Path

import yaml

from .catalog import is_key

PREFIX = "rule:"


def parse_tag(tag: str) -> str | None:
    """Return the rule key in a tag such as '@rule:cms:ee:EE21', or None if it is not a rule tag."""
    t = tag.strip().lstrip("@")
    if not t.startswith(PREFIX):
        return None
    return t[len(PREFIX):]


def split_values(value: str) -> list[str]:
    return [v for v in re.split(r"[\s,]+", value or "") if v]


class Sidecar:
    def __init__(self, mapping: dict[str, list[str]] | None = None):
        self.mapping = mapping or {}

    @classmethod
    def load(cls, path: str | Path | None) -> Sidecar:
        if not path or not Path(path).exists():
            return cls()
        data = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
        return cls({str(k): ([v] if isinstance(v, str) else list(v)) for k, v in data.items()})

    def keys_for(self, test_id: str) -> list[str]:
        out: list[str] = []
        for pattern, keys in self.mapping.items():
            if fnmatch.fnmatchcase(test_id, pattern):
                out.extend(keys)
        return out


def invalid_keys(keys) -> list[str]:
    return [k for k in keys if not is_key(k)]
