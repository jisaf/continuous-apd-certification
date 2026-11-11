from pathlib import Path

from capd_trx import TrxSource

from capd.connectors import base
from capd.connectors.testing import check_source

FIX = Path(__file__).parent / "fixtures"


def test_conforms_to_the_integration_contract():
    # The shared conformance kit: schema-valid records, valid rule keys, inferred programs.
    check_source(TrxSource(), {"paths": [str(FIX / "sample.trx")]})


def test_reads_categories_outcomes_and_ids():
    records = check_source(TrxSource(), {"paths": [str(FIX / "sample.trx")]})
    by_id = {r["testId"]: r for r in records}
    multi = by_id["Eligibility.Tests.MultiBenefitTests::PendsSnapWithoutHoldingMedicaid"]
    assert multi["ruleIds"] == ["cms:ee:EE21"] and multi["result"] == "pass"
    assert multi["programs"] == ["medicaid", "snap"]
    assert by_id["Eligibility.Tests.SnapBudgetTests::CalculatesStandardDeduction"]["result"] == "fail"
    assert by_id["Eligibility.Tests.Helpers::UntaggedHelper"]["ruleIds"] == []


def test_is_registered_as_a_plugin():
    # Works once the package is installed (pip install -e .): capd finds it through the entry point.
    assert "trx" in base.available()
    assert isinstance(base.get("trx"), TrxSource)
