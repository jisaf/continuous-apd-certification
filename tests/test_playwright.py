from capd.connectors import base
from capd.connectors.playwright import PlaywrightSource
from capd.connectors.testing import check_source

from .conftest import FIX


def test_playwright_tags_retries_and_ids():
    records = check_source(PlaywrightSource(), {"paths": [str(FIX / "playwright.json")]})
    by_id = {r["testId"]: r for r in records}
    multi = by_id["apply.spec.ts::Multi-benefit application › pends SNAP without holding Medicaid [chromium]"]
    assert multi["result"] == "pass" and multi["attempts"] == 2                 # failed, then passed on retry
    assert multi["ruleIds"] == ["cms:ee:EE1", "cms:ee:EE21"]                     # describe tag + test tag
    assert multi["programs"] == ["medicaid", "snap"]
    notice = by_id["apply.spec.ts::Multi-benefit application › shows the notice in the preferred language [chromium]"]
    assert notice["result"] == "fail" and notice["ruleIds"] == ["cms:ee:EE1", "cms:ee:EE10"]   # title tag, timeout = fail
    skipped = by_id["apply.spec.ts::Multi-benefit application › skipped flow [chromium]"]
    assert skipped["result"] == "skipped"


def test_playwright_is_registered():
    assert isinstance(base.get("playwright"), PlaywrightSource)
