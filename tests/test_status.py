from capd.status import evaluate

RULE = {"gates": {"ORR": ["test"], "CR": ["metric"]}, "freshnessDays": 30, "acceptance": "not_required"}
DOC = {"gates": {"ORR": ["document"]}, "freshnessDays": 365, "acceptance": "required"}
T = lambda r, d="2026-11-10": {"kind": "test", "result": r, "observedAt": d + "T00:00:00Z", "environment": "ci"}  # noqa: E731


def test_order_of_statuses():
    asof = "2026-11-11"
    assert evaluate(RULE, "ORR", [], as_of=asof, na_accepted=True) == "N/A"
    assert evaluate(RULE, "ORR", [T("pass")], as_of=asof, disputed=True) == "Disputed"
    assert evaluate(RULE, "ORR", [], as_of=asof) == "No evidence"
    assert evaluate(RULE, "ORR", [T("skipped")], as_of=asof) == "No evidence"
    assert evaluate(RULE, "ORR", [T("pass"), T("fail")], as_of=asof) == "Not met"
    assert evaluate(RULE, "ORR", [T("pass", "2026-09-01")], as_of=asof) == "Stale"
    assert evaluate(RULE, "ORR", [T("pass")], as_of=asof) == "Met"


def test_tests_are_never_at_risk_from_a_far_gate():
    assert evaluate(RULE, "ORR", [T("pass")], as_of="2026-11-11", gate_date="2027-06-01") == "Met"


def test_expiring_documents_and_acceptance():
    doc = {"kind": "document", "result": "present", "observedAt": "2026-01-15T00:00:00Z"}
    assert evaluate(DOC, "ORR", [doc], as_of="2026-11-11", gate_date="2027-03-01") == "At risk"
    fresh = dict(doc, observedAt="2026-11-01T00:00:00Z")
    assert evaluate(DOC, "ORR", [fresh], as_of="2026-11-11", gate_date="2027-03-01") == "Awaiting acceptance"
    assert evaluate(DOC, "ORR", [fresh], as_of="2026-11-11", gate_date="2027-03-01", accepted=True) == "Met"


def test_cr_metrics_must_come_from_production():
    m = {"kind": "metric", "result": "value", "observedAt": "2026-11-01T00:00:00Z", "environment": "ci"}
    assert evaluate(RULE, "CR", [m], as_of="2026-11-11") == "No evidence"
    assert evaluate(RULE, "CR", [dict(m, environment="production")], as_of="2026-11-11") == "Met"
