"""Step definitions for the Gherkin features (run with pytest-bdd; write Cucumber JSON with --cucumberjson)."""

from pathlib import Path

from pytest_bdd import given, parsers, scenarios, then, when

from adapter import determine

scenarios(str(Path(__file__).resolve().parents[1] / "features"))


@given(parsers.parse("an Illinois household of {size:d} people with no income"), target_fixture="case")
def household(size):
    return {"id": f"feature-il-{size}", "state": "IL", "household": {"size": size}}


@when("the system determines SNAP eligibility", target_fixture="result")
def run(case):
    return determine(case)


@then("the household is eligible")
def eligible(result):
    assert result["eligible"] is True


@then(parsers.parse("the monthly benefit is ${benefit:d}"))
def benefit(result, benefit):
    assert result["monthlyBenefit"] == benefit
