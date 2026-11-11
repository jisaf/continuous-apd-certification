"""pytest plugin (installed automatically with capd): tag tests with rule keys.

    import pytest

    @pytest.mark.rule("fna:sirt:S0215", "cms:ee:EE15")
    def test_standard_deduction(): ...

Each key is written to the JUnit XML report as <property name="rule" value="..."/>, which the
junit source connector reads. Run pytest with --junitxml=out/junit.xml -o junit_family=xunit1
(pytest only writes record_property values in the xunit1 family).

With pytest-bdd, Gherkin tags such as @rule:cms:ee:EE21 become the same rule marks.
"""

from __future__ import annotations

import pytest


def pytest_configure(config):
    config.addinivalue_line("markers", "rule(*keys): certification rule keys this test proves, e.g. rule('cms:ee:EE21')")


@pytest.fixture(autouse=True)
def _capd_rule_properties(request, record_property):
    for mark in request.node.iter_markers("rule"):
        for key in mark.args:
            record_property("rule", key)
    yield


@pytest.hookimpl(optionalhook=True)
def pytest_bdd_apply_tag(tag, function):
    """pytest-bdd: turn a Gherkin @rule:<key> tag into a rule mark instead of an unknown mark."""
    if tag.startswith("rule:"):
        pytest.mark.rule(tag[len("rule:"):])(function)
        return True
    return None
