import copy

from capd.checktags import check
from capd.compare import compare, markdown
from capd.connectors.junit import JUnitSource
from capd.evidence import build_bundle, load, save

from .conftest import FIX


def bundle(ctx, results: dict[str, str]):
    recs = JUnitSource().collect(ctx, {"paths": [str(FIX / "junit.xml")]})
    for r in recs:
        if r["testId"] in results:
            r["result"] = results[r["testId"]]
    return build_bundle(ctx, recs, ctx.warnings)


SD = "tests.test_rules::test_standard_deduction"
EI = "tests.test_rules::test_earned_income"


def test_regression_fixed_and_quarantine(ctx):
    base = bundle(ctx, {EI: "fail"})
    cur = bundle(ctx, {SD: "fail"})
    res = compare(cur, base)
    assert [r["testId"] for r in res["regressions"]] == [SD]
    assert [r["testId"] for r in res["fixed"]] == [EI]
    assert not res["blocking"]                                          # report-only by default
    assert compare(cur, base, mode="blocking")["blocking"]
    q = compare(cur, base, quarantine={SD}, mode="blocking")
    assert not q["blocking"] and [r["testId"] for r in q["quarantined"]] == [SD]


def test_untagged_failures_never_count(ctx):
    base = bundle(ctx, {})
    cur = bundle(ctx, {"tests.test_misc::test_untagged": "fail"})
    assert compare(cur, base)["regressions"] == []


def test_no_baseline_reports_new_failures(ctx):
    res = compare(bundle(ctx, {SD: "fail"}), None)
    assert res["regressions"] == [] and [r["testId"] for r in res["newFailures"]] == [SD]


def test_markdown_is_one_sticky_comment(ctx):
    md = markdown(compare(bundle(ctx, {SD: "fail"}), bundle(ctx, {})))
    assert md.startswith("<!-- capd-certification-report -->") and "1 certification regression" in md


def test_bundle_hash_detects_tampering(ctx, tmp_path):
    b = bundle(ctx, {})
    save(b, tmp_path / "b.json")
    assert load(tmp_path / "b.json")["recordsSha256"] == b["recordsSha256"]
    bad = copy.deepcopy(b)
    bad["records"][0]["result"] = "fail"
    save(bad, tmp_path / "bad.json")
    try:
        load(tmp_path / "bad.json")
        raise AssertionError("tampered bundle accepted")
    except ValueError as e:
        assert "recordsSha256" in str(e)


def test_check_tags(ctx, catalog):
    b = bundle(ctx, {})
    issues = check(b, catalog, ["tests.test_misc::*"])
    assert any("cms:ee:EE999" in i for i in issues)
    assert any("untagged test in a tagged path: tests.test_misc::test_untagged" in i for i in issues)
    assert check(b, catalog, []) == [i for i in issues if "untagged" not in i]
