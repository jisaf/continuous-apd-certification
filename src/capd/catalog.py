"""The rules catalog: CMS and FNA certification rules with stable keys."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from importlib import resources

KEY_RE = re.compile(r"^(cms|fna|state):[a-z]+:[A-Za-z0-9.\-]+$")
GATES = ("ORR", "CR", "FNA-UAT", "FNA-PILOT")
PROGRAM_BY_AGENCY = {"cms": ["medicaid"], "fna": ["snap"]}


def is_key(text: str) -> bool:
    return bool(KEY_RE.match(text or ""))


@dataclass
class Catalog:
    version: str
    rules: dict[str, dict]
    indicators: list[dict] = field(default_factory=list)

    @classmethod
    def load(cls, state_rules: list[dict] | None = None, overrides: dict | None = None) -> Catalog:
        raw = json.loads(resources.files("capd.data.catalog").joinpath("catalog.json").read_text(encoding="utf-8"))
        rules = {r["key"]: dict(r) for r in raw["rules"]}
        for r in state_rules or []:
            rules[r["key"]] = dict(r)
        for key, ov in (overrides or {}).items():
            if key in rules:
                rules[key].update(ov)
        return cls(raw["catalogVersion"], rules, raw.get("indicators", []))

    def __contains__(self, key: str) -> bool:
        return key in self.rules

    def get(self, key: str) -> dict | None:
        return self.rules.get(key)

    def applicable(self, key: str) -> bool:
        r = self.rules.get(key)
        return bool(r) and r.get("applicable", True)

    def programs_for(self, keys) -> list[str]:
        """Infer programs from rule keys, so nobody tags programs by hand."""
        out: list[str] = []
        for k in keys:
            r = self.rules.get(k)
            progs = r["programs"] if r else PROGRAM_BY_AGENCY.get(k.split(":", 1)[0], [])
            for p in progs:
                if p not in out:
                    out.append(p)
        return sorted(out)

    def rules_for_gate(self, gate: str) -> list[dict]:
        return [r for r in self.rules.values() if gate in r.get("gates", {}) and r.get("applicable", True)]

    def summary(self) -> dict:
        by_set: dict[str, int] = {}
        for r in self.rules.values():
            by_set[f"{r['agency']}:{r['set']}"] = by_set.get(f"{r['agency']}:{r['set']}", 0) + 1
        return {"version": self.version, "rules": len(self.rules), "bySet": by_set}
