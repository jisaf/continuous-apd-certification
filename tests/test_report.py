import re

from capd.compare import compare
from capd.connectors.junit import JUnitSource
from capd.connectors.sarif import SarifSource
from capd.evidence import build_bundle
from capd.report.html import render

from .conftest import FIX


def make(ctx):
    recs = JUnitSource().collect(ctx, {"paths": [str(FIX / "junit.xml")]})
    recs += SarifSource().collect(ctx, {"paths": [str(FIX / "security.sarif")], "includeCounts": True})
    return build_bundle(ctx, recs, ctx.warnings)


def test_self_contained_and_pipeline_only(ctx, catalog):
    b = make(ctx)
    html = render(b, catalog, compare(b, None))
    assert "<script" not in html.lower()                       # no scripts at all
    assert not re.search(r'(src|href)="https?://', html)        # nothing loaded from outside
    assert 'lang="en"' in html and "<th scope=col>" in html     # basic accessibility markup
    assert "findings" not in html and "failing" not in html.split("Scans")[1].split("Tag checks")[0]
    assert "Security scan (codeql)" in html and ">Fail<" in html
    assert "not a CMS or FNA finding" in html


def test_regressions_are_listed(ctx, catalog):
    base = make(ctx)
    recs = [dict(r) for r in base["records"]]
    for r in recs:
        if r.get("testId") == "tests.test_rules::test_standard_deduction":
            r["result"] = "fail"
    cur = build_bundle(ctx, recs)
    html = render(cur, catalog, compare(cur, base))
    assert "Regressions (1)" in html and "test_standard_deduction" in html


def test_html_is_escaped(ctx, catalog):
    b = make(ctx)
    b["records"][0]["name"] = "<img src=x onerror=alert(1)>"
    b["build"]["id"] = "<b>"
    html = render(b, catalog, None)
    assert "<img src=x" not in html and "&lt;b&gt;" in html
