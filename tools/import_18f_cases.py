"""Convert the 18F SNAP API prototype's Gherkin scenarios into the toolkit's golden test case format.

Source: https://github.com/18F/snap-api-prototype (commit 215f3f3b, 2020-08-17), a U.S. government work
with a CC0 1.0 waiver, so the converted cases are CC0 too. The expected values are 18F's, computed for
FY2020 federal parameters and the named states. They are historical samples that show the format and
exercise the sample system; a state must recompute expected values for its own rules and current year.

Run:  python tools/import_18f_cases.py /path/to/snap-api-prototype
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "examples" / "golden-cases" / "snap"
COMMIT = "215f3f3b52e7243eaa9ea05dd86f647b6af35648"
FILES = ["il.feature", "ut.feature", "vt.feature"]

STEPS = [
    (r"the household is in (\w+)", lambda m, h: h.__setitem__("state", m[1])),
    (r"(no|an) emergency allotment waiver", lambda m, h: h.__setitem__("emergencyAllotment", m[1] == "an")),
    (r"a (\d+)-person household", lambda m, h: h.__setitem__("size", int(m[1]))),
    (r"the household (does|does not) include an elderly or disabled member", lambda m, h: h.__setitem__("elderlyOrDisabled", m[1] == "does")),
    (r"the household has earned income of \$(\d+) monthly", lambda m, h: h.__setitem__("earnedIncome", int(m[1]))),
    (r"the household has other income of \$(\d+) monthly", lambda m, h: h.__setitem__("otherIncome", int(m[1]))),
    (r"the household has assets of \$(\d+)", lambda m, h: h.__setitem__("assets", int(m[1]))),
    (r"the household has dependent care costs of \$(\d+) monthly", lambda m, h: h.__setitem__("dependentCare", int(m[1]))),
    (r"the household has medical expenses for elderly or disabled members of \$(\d+) monthly", lambda m, h: h.__setitem__("medicalExpenses", int(m[1]))),
    (r"the household has court-ordered child support payments of \$(\d+) monthly", lambda m, h: h.__setitem__("childSupportPaid", int(m[1]))),
    (r"the household has rent or mortgage costs of \$(\d+) monthly", lambda m, h: h.__setitem__("rentOrMortgage", int(m[1]))),
    (r"the household has homeowners insurance and taxes costs of \$(\d+) monthly", lambda m, h: h.__setitem__("homeownersInsuranceAndTaxes", int(m[1]))),
    (r"the household pays for AC or heat", lambda m, h: h.__setitem__("utilityAllowance", "HEATING_AND_COOLING")),
    (r"the household pays for water and trash", lambda m, h: h.__setitem__("utilityAllowance", "BASIC_LIMITED_ALLOWANCE")),
    (r"the household pays for a single utility", lambda m, h: h.__setitem__("utilityAllowance", "SINGLE_UTILITY_ALLOWANCE")),
    (r"the household pays phone bills only", lambda m, h: h.__setitem__("utilityAllowance", "PHONE")),
    (r"the household is not billed separately for any utilities", lambda m, h: h.__setitem__("utilityAllowance", "NONE")),
    (r"the household has utility costs of \$(\d+) monthly", lambda m, h: h.__setitem__("utilityCosts", int(m[1]))),
]
EXPECT = [
    (r"the family is likely (not eligible|eligible)", lambda m, e: e.__setitem__("eligible", m[1] == "eligible")),
    (r"the estimated benefit is \$(\d+) per month", lambda m, e: e.__setitem__("monthlyBenefit", int(m[1]))),
]
# SIRT rows (by FNA ID) that a case exercises, depending on its facts.
SIRT_BY_FACT = {
    None: ["OD-1"],                       # standard deduction by household size
    "earnedIncome": ["EI-13"],            # earned income deduction
    "dependentCare": ["DD-1"],            # dependent care expenses
    "medicalExpenses": ["MD-2"],          # excess medical deduction
    "childSupportPaid": ["OD-3"],         # child support deduction
    "assets": ["R-1"],                    # resource test
}
SHELTER = {False: "SD-27", True: "SD-28"}  # excess shelter, without / with an elderly or disabled member
UTILITY = {"HEATING_AND_COOLING": "SD-24", "BASIC_LIMITED_ALLOWANCE": "SD-25", "SINGLE_UTILITY_ALLOWANCE": "SD-26"}


def sirt_keys() -> dict[str, str]:
    cat = json.loads((ROOT / "src/capd/data/catalog/catalog.json").read_text())
    out: dict[str, str] = {}
    for r in cat["rules"]:
        if r["set"] == "sirt":
            out.setdefault(r["sourceId"], r["key"])  # first row with that FNA ID
    return out


def rules_for(h: dict, keys: dict[str, str]) -> list[str]:
    ids = list(SIRT_BY_FACT[None])
    for fact, sids in SIRT_BY_FACT.items():
        if fact and h.get(fact):
            ids += sids
    if h.get("rentOrMortgage") or h.get("homeownersInsuranceAndTaxes"):
        ids.append(SHELTER[bool(h.get("elderlyOrDisabled"))])
    if h.get("utilityAllowance") in UTILITY:
        ids.append(UTILITY[h["utilityAllowance"]])
    return sorted({keys[i] for i in ids})


def parse(path: Path, keys: dict[str, str]) -> list[dict]:
    background: dict = {}
    cases, current, in_background = [], None, False
    for n, raw in enumerate(path.read_text().splitlines(), start=1):
        line = raw.strip()
        if line.startswith("Background:"):
            in_background = True
            continue
        if line.startswith("Scenario"):
            in_background = False
            current = {"household": dict(background), "expected": {}, "line": n, "title": line.partition(":")[2].strip()}
            cases.append(current)
            continue
        step = re.sub(r"^(Given|And|When|Then)\s+", "", line)
        target = background if in_background else (current["household"] if current else None)
        if target is None:
            continue
        for pat, fn in STEPS:
            m = re.search(pat, step)
            if m:
                fn(m, target)
        if current:
            for pat, fn in EXPECT:
                m = re.search(pat, step)
                if m:
                    fn(m, current["expected"])
    out = []
    state = path.stem.upper()
    for i, c in enumerate(cases, start=1):
        h = c["household"]
        out.append({
            "id": f"snap-18f-{path.stem}-{i:02d}",
            "program": "snap",
            "state": h.pop("state", state),
            "policyPeriod": "FY2020",
            "rules": rules_for(h, keys),
            "title": c["title"] or f"{state} scenario {i}",
            "source": {"name": "18F SNAP API prototype", "url": "https://github.com/18F/snap-api-prototype",
                       "file": f"features/{path.name}@{COMMIT[:8]}", "line": c["line"], "license": "CC0-1.0 (U.S. government work)"},
            "household": h,
            "expected": c["expected"],
            "status": "active",
        })
    return out


def main(repo: str) -> None:
    keys = sirt_keys()
    OUT.mkdir(parents=True, exist_ok=True)
    total = 0
    for name in FILES:
        cases = parse(Path(repo) / "features" / name, keys)
        header = (f"# Golden cases converted from 18F snap-api-prototype {name} (commit {COMMIT[:8]}).\n"
                  "# CC0 1.0. Historical FY2020 values: a state must recompute expected values for its own rules and year.\n")
        (OUT / f"18f-{Path(name).stem}.yaml").write_text(header + yaml.safe_dump(cases, sort_keys=False, allow_unicode=True))
        total += len(cases)
    print(f"wrote {total} cases to {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: python tools/import_18f_cases.py /path/to/snap-api-prototype "
                 "(git clone https://github.com/18F/snap-api-prototype)")
    main(sys.argv[1])
