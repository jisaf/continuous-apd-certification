"""Run every golden case through the system adapter. Each case's rule keys become pytest rule marks,
so the JUnit XML report carries them to capd."""

from pathlib import Path

import pytest
import yaml

from adapter import determine

CASES_DIR = Path(__file__).resolve().parents[2] / "golden-cases" / "snap"


def load_cases():
    params = []
    for f in sorted(CASES_DIR.glob("*.yaml")):
        for case in yaml.safe_load(f.read_text()):
            if case.get("status", "active") != "active":
                continue  # disputed or retired cases are excluded until resolved
            params.append(pytest.param(case, id=case["id"], marks=pytest.mark.rule(*case["rules"])))
    return params


@pytest.mark.parametrize("case", load_cases())
def test_golden_case(case):
    got = determine(case)
    exp = case["expected"]
    assert got["eligible"] == exp["eligible"], f"eligibility: system {got['eligible']}, expected {exp['eligible']}"
    if "monthlyBenefit" in exp:
        assert got["monthlyBenefit"] == exp["monthlyBenefit"], f"benefit: system {got['monthlyBenefit']}, expected {exp['monthlyBenefit']}"
