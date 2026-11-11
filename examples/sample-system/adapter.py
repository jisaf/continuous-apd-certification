"""System adapter: map a golden test case to the sample system's determination API.

A vendor writes one adapter like this for its own system. It is small when the system exposes a
test-facing determination API (household facts in, decision out), as this one does.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "vendor"))

from snap_financial_factors.benefit_estimate.snap_estimate_entrypoint import SnapEstimateEntrypoint  # noqa: E402

FIELDS = {
    "size": "household_size",
    "elderlyOrDisabled": "household_includes_elderly_or_disabled",
    "earnedIncome": "monthly_job_income",
    "otherIncome": "monthly_non_job_income",
    "assets": "resources",
    "dependentCare": "dependent_care_costs",
    "medicalExpenses": "medical_expenses_for_elderly_or_disabled",
    "childSupportPaid": "court_ordered_child_support_payments",
    "rentOrMortgage": "rent_or_mortgage",
    "homeownersInsuranceAndTaxes": "homeowners_insurance_and_taxes",
    "utilityAllowance": "utility_allowance",
    "utilityCosts": "utility_costs",
    "emergencyAllotment": "use_emergency_allotment",
}
DEFAULTS = {"monthly_job_income": 0, "monthly_non_job_income": 0, "resources": 0,
            "household_includes_elderly_or_disabled": False}


def _simulated_bug() -> None:
    """For the demo only: CAPD_DEMO_BUG=standard-deduction makes the system ignore the standard deduction."""
    if os.environ.get("CAPD_DEMO_BUG") != "standard-deduction":
        return
    from snap_financial_factors.deductions import standard_deduction as sd
    from snap_financial_factors.deductions.deduction_result import DeductionResult

    sd.StandardDeduction.calculate = lambda self: DeductionResult(result=0, explanation=["(simulated bug)"])


def determine(case: dict) -> dict:
    """Return {'eligible': bool, 'monthlyBenefit': int} for a SNAP golden case."""
    _simulated_bug()
    data = dict(DEFAULTS)
    data["state_or_territory"] = case["state"]
    for k, v in case["household"].items():
        data[FIELDS[k]] = v
    result = SnapEstimateEntrypoint(data).calculate()
    if result["status"] != "OK":
        raise ValueError(f"{case['id']}: system rejected input: {result.get('errors')}")
    return {"eligible": result["eligible"], "monthlyBenefit": result["estimated_monthly_benefit"]}
