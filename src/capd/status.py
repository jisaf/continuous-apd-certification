"""Reference rule-status logic.

The report layer implements the same definitions in SQL (report-layer/sql/30_rule_status.sql); the test
suite checks that both agree. The pipeline never decides Met: status needs acceptance records and external
evidence that only the report layer holds. Met is a readiness signal, not an agency finding.

Order of evaluation (first match wins):
  N/A  ->  Disputed  ->  No evidence  ->  Not met  ->  Stale  ->  At risk  ->  Awaiting acceptance  ->  Met
"""

from __future__ import annotations

from datetime import date, datetime

GATE_ENVIRONMENTS = {"CR": {"production"}, "FNA-PILOT": {"pilot", "production"}}
EXTERNAL_KINDS = {"document", "attestation", "demonstration", "assessment"}
# Evidence that is produced once and can expire before a gate. Tests, scans and metrics are refreshed by
# every build or month, so they can be Stale but are never "At risk" because of a far-off gate date.
EXPIRING_KINDS = EXTERNAL_KINDS | {"report"}


def _d(value) -> date:
    if isinstance(value, date) and not isinstance(value, datetime):
        return value
    if isinstance(value, datetime):
        return value.date()
    return datetime.fromisoformat(str(value).replace("Z", "+00:00")).date()


def evaluate(rule: dict, gate: str, evidence: list[dict], *, as_of, gate_date=None,
             accepted: bool = False, disputed: bool = False, na_accepted: bool = False,
             min_tests: int = 1) -> str:
    """evidence: rows with kind, result, observedAt, environment for this rule (latest run's tests, plus tracked items)."""
    if na_accepted:
        return "N/A"
    if disputed:
        return "Disputed"
    required = rule.get("gates", {}).get(gate, [])
    envs = GATE_ENVIRONMENTS.get(gate)
    as_of, gate_date = _d(as_of), (_d(gate_date) if gate_date else None)
    freshness = int(rule.get("freshnessDays", 30))
    latest_dates = []
    expiring_dates = []
    failing = False
    for kind in required:
        # Environment matters only for metrics: production data for the CR, pilot or production for the pilot.
        rows = [e for e in evidence if e["kind"] == kind and (envs is None or kind != "metric" or e.get("environment") in envs)]
        if kind == "test":
            counted = [e for e in rows if e["result"] in ("pass", "fail", "error")]
            if len([e for e in counted if e["result"] == "pass"]) < min_tests and not any(e["result"] in ("fail", "error") for e in counted):
                return "No evidence"
            if any(e["result"] in ("fail", "error") for e in counted):
                failing = True
            latest_dates.append(min(_d(e["observedAt"]) for e in counted))
        else:
            if not rows:
                return "No evidence"
            last = max(rows, key=lambda e: _d(e["observedAt"]))
            if last["result"] in ("fail", "error"):
                failing = True
            latest_dates.append(_d(last["observedAt"]))
            if kind in EXPIRING_KINDS:
                expiring_dates.append(_d(last["observedAt"]))
    if not required:
        return "No evidence"
    if failing:
        return "Not met"
    oldest = min(latest_dates)
    if (as_of - oldest).days > freshness:
        return "Stale"
    if gate_date and expiring_dates and (gate_date - min(expiring_dates)).days > freshness:
        return "At risk"
    if rule.get("acceptance") == "required" and not accepted:
        return "Awaiting acceptance"
    return "Met"
