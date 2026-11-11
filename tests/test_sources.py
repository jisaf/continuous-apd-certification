from capd.connectors.axe import AxeSource
from capd.connectors.cucumber import CucumberSource
from capd.connectors.junit import JUnitSource
from capd.connectors.sarif import SarifSource
from capd.connectors.testing import check_source

from .conftest import FIX


def by_id(records):
    return {r.get("testId"): r for r in records}


def test_junit_tags_reruns_and_warnings(ctx):
    recs = by_id(JUnitSource().collect(ctx, {"paths": [str(FIX / "junit.xml")]}))
    assert recs["tests.test_rules::test_standard_deduction"]["ruleIds"] == ["fna:sirt:S0215"]
    rerun = recs["tests.test_rules::test_earned_income"]
    assert rerun["result"] == "pass" and rerun["attempts"] == 2          # failed once, passed on rerun
    assert rerun["programs"] == ["medicaid", "snap"]                      # inferred from the keys
    assert recs["tests.test_rules::test_skipped"]["result"] == "skipped"
    assert recs["tests.test_rules::test_skipped"]["ruleIds"] == ["cms:ee:EE5", "cms:ee:EE6"]
    assert recs["tests.test_rules::test_unknown_key"]["ruleIds"] == []
    assert any("cms:ee:EE999" in w for w in ctx.warnings)
    assert recs["tests.test_misc::test_untagged"]["ruleIds"] == []


def test_junit_exclude(ctx):
    recs = JUnitSource().collect(ctx, {"paths": [str(FIX / "junit.xml")], "exclude": ["tests.test_misc::*"]})
    assert "tests.test_misc::test_untagged" not in by_id(recs)


def test_cucumber_feature_tags_outlines_and_status(ctx):
    recs = by_id(CucumberSource().collect(ctx, {"paths": [str(FIX / "cucumber.json")]}))
    first = recs["features/notices.feature::notices;denial-notice;;2"]
    assert first["ruleIds"] == ["cms:ee:EE9", "fna:sirt:S0215"] and first["result"] == "pass"
    second = recs["features/notices.feature::notices;denial-notice;;3"]   # same name, different example row
    assert second["result"] == "fail" and second["ruleIds"] == ["cms:ee:EE9"]
    assert recs["features/notices.feature::notices;pending"]["result"] == "error"
    assert len(recs) == 3                                                 # background is not a test


def test_sarif_pass_fail_without_counts(ctx):
    recs = SarifSource().collect(ctx, {"paths": [str(FIX / "security.sarif")], "failAt": "warning"})
    res = {r["detail"]["tool"]: r for r in recs}
    assert res["semgrep"]["result"] == "pass" and res["codeql"]["result"] == "fail"
    assert "findings" not in res["codeql"]["detail"]                      # counts stay in the report layer
    with_counts = SarifSource().collect(ctx, {"paths": [str(FIX / "security.sarif")], "includeCounts": True})
    assert any("findings" in r["detail"] for r in with_counts)


def test_axe(ctx):
    recs = by_id(AxeSource().collect(ctx, {"paths": [str(FIX / "axe.json")]}))
    assert recs["scan::accessibility::https://example.test/apply"]["result"] == "pass"
    assert recs["scan::accessibility::https://example.test/status"]["result"] == "fail"
    assert recs["scan::accessibility::https://example.test/status"]["ruleIds"] == ["cms:cef:CEF12"]


def test_builtin_sources_pass_the_conformance_kit():
    check_source(JUnitSource(), {"paths": [str(FIX / "junit.xml")]})
    check_source(CucumberSource(), {"paths": [str(FIX / "cucumber.json")]})
    check_source(SarifSource(), {"paths": [str(FIX / "security.sarif")]})
    check_source(AxeSource(), {"paths": [str(FIX / "axe.json")]})
