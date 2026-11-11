-- Report layer views (portable SQL: Snowflake and DuckDB). Run after 10_tables.sql.
-- Status definitions match capd.status (Python); the test suite checks they agree.

-- The latest build on main.
CREATE OR REPLACE VIEW V_LATEST_MAIN_BUILD AS
SELECT build_id, MAX(generated_at) AS generated_at
FROM EVIDENCE
WHERE branch = 'main'
GROUP BY build_id
QUALIFY ROW_NUMBER() OVER (ORDER BY MAX(generated_at) DESC) = 1;

-- Test and scan evidence per rule from the latest main build.
CREATE OR REPLACE VIEW V_TEST_EVIDENCE AS
SELECT e.rule_key,
       e.kind,
       COUNT(*)                                                    AS tests,
       SUM(CASE WHEN e.result = 'pass' THEN 1 ELSE 0 END)           AS passing,
       SUM(CASE WHEN e.result IN ('fail', 'error') THEN 1 ELSE 0 END) AS failing,
       MIN(e.observed_at)                                          AS observed_at
FROM EVIDENCE e
JOIN V_LATEST_MAIN_BUILD b ON e.build_id = b.build_id
WHERE e.rule_key IS NOT NULL AND e.kind IN ('test', 'scan')
GROUP BY e.rule_key, e.kind;

-- Per rule, gate and required kind: is the evidence missing, failing, or ok, and how old is it?
CREATE OR REPLACE VIEW V_RULE_KIND_EVIDENCE AS
WITH req AS (
  SELECT g.rule_key, g.gate, g.kind, r.freshness_days, r.acceptance
  FROM RULE_GATES g JOIN RULES r ON r.rule_key = g.rule_key
  WHERE r.applicable
),
other_latest AS (   -- latest non-test evidence of each kind: metrics from the pipeline, tracked items from the state
  SELECT rule_key, kind, environment, result, observed_at FROM (
    SELECT rule_key, kind, environment, result, observed_at FROM EVIDENCE WHERE kind NOT IN ('test', 'scan')
    UNION ALL
    SELECT rule_key, kind, NULL AS environment, result, observed_at FROM TRACKED_ITEMS
    WHERE rule_key IS NOT NULL AND status = 'complete'
  ) x
)
SELECT q.rule_key, q.gate, q.kind, q.freshness_days, q.acceptance,
       CASE
         WHEN q.kind = 'test' THEN
           CASE WHEN COALESCE(t.failing, 0) > 0 THEN 'fail'
                WHEN COALESCE(t.passing, 0) >= 1 THEN 'ok'
                ELSE 'missing' END
         ELSE
           CASE WHEN o.result IS NULL THEN 'missing'
                WHEN o.result IN ('fail', 'error') THEN 'fail'
                ELSE 'ok' END
       END AS kind_state,
       CASE WHEN q.kind = 'test' THEN t.observed_at ELSE o.observed_at END AS observed_at
FROM req q
LEFT JOIN V_TEST_EVIDENCE t ON t.rule_key = q.rule_key AND t.kind = 'test' AND q.kind = 'test'
LEFT JOIN (
  SELECT ol.*, ROW_NUMBER() OVER (PARTITION BY rule_key, kind, gate ORDER BY observed_at DESC) AS rn, g.gate
  FROM other_latest ol
  CROSS JOIN (SELECT DISTINCT gate FROM RULE_GATES) g
  WHERE ol.kind <> 'metric'                       -- environment matters only for metrics
     OR (g.gate = 'CR' AND ol.environment = 'production')
     OR (g.gate = 'FNA-PILOT' AND ol.environment IN ('pilot', 'production'))
     OR (g.gate NOT IN ('CR', 'FNA-PILOT'))
) o ON o.rule_key = q.rule_key AND o.kind = q.kind AND o.gate = q.gate AND o.rn = 1 AND q.kind <> 'test';

-- Latest acceptance decision per rule and gate.
CREATE OR REPLACE VIEW V_LATEST_DECISION AS
SELECT rule_key, gate, decision, role, decided_at
FROM ACCEPTANCES
QUALIFY ROW_NUMBER() OVER (PARTITION BY rule_key, gate ORDER BY decided_at DESC) = 1;

-- Rule status per gate. Order: N/A, Disputed, No evidence, Not met, Stale, At risk, Awaiting acceptance, Met.
-- Met is the toolkit's readiness signal, not CMS's "Evidence Satisfactory" or FNA's concurrence.
CREATE OR REPLACE VIEW V_RULE_STATUS AS
WITH agg AS (
  SELECT rule_key, gate, MAX(freshness_days) AS freshness_days, MAX(acceptance) AS acceptance,
         SUM(CASE WHEN kind_state = 'missing' THEN 1 ELSE 0 END) AS missing,
         SUM(CASE WHEN kind_state = 'fail' THEN 1 ELSE 0 END)    AS failing,
         MIN(observed_at)                                        AS oldest,
         -- only evidence that is produced once can expire before a gate (tests and metrics refresh)
         MIN(CASE WHEN kind IN ('document', 'attestation', 'demonstration', 'assessment', 'report')
                  THEN observed_at END)                          AS oldest_expiring
  FROM V_RULE_KIND_EVIDENCE
  GROUP BY rule_key, gate
)
SELECT a.rule_key, a.gate, r.agency, r.rule_set, r.source_id, r.title, r.responsibility, r.coverage,
       d.decision AS latest_decision, g.planned_date AS gate_date, a.oldest AS evidence_as_of,
       CASE
         WHEN d.decision = 'na_accepted' THEN 'N/A'
         WHEN d.decision = 'disputed' THEN 'Disputed'
         WHEN a.missing > 0 THEN 'No evidence'
         WHEN a.failing > 0 THEN 'Not met'
         WHEN DATEDIFF('day', CAST(a.oldest AS DATE), CURRENT_DATE) > a.freshness_days THEN 'Stale'
         WHEN g.planned_date IS NOT NULL AND a.oldest_expiring IS NOT NULL
              AND DATEDIFF('day', CAST(a.oldest_expiring AS DATE), g.planned_date) > a.freshness_days THEN 'At risk'
         WHEN a.acceptance = 'required' AND COALESCE(d.decision, '') <> 'accepted' THEN 'Awaiting acceptance'
         ELSE 'Met'
       END AS status
FROM agg a
JOIN RULES r ON r.rule_key = a.rule_key
LEFT JOIN V_LATEST_DECISION d ON d.rule_key = a.rule_key AND d.gate = a.gate
LEFT JOIN GATES g ON g.gate = a.gate;

-- Gate blockers: a list, never a percentage, so many small rows cannot hide one missing letter.
CREATE OR REPLACE VIEW V_GATE_BLOCKERS AS
SELECT gate, rule_key AS item, source_id, title, responsibility, status AS reason, gate_date
FROM V_RULE_STATUS
WHERE status IN ('No evidence', 'Not met', 'Stale', 'Disputed', 'At risk')
UNION ALL
SELECT gate, item_key AS item, NULL AS source_id, title, owner AS responsibility,
       'Overdue tracked item' AS reason, due_date AS gate_date
FROM TRACKED_ITEMS
WHERE status <> 'complete' AND due_date < CURRENT_DATE;

-- One calendar: planned gates and tracked due dates in order.
CREATE OR REPLACE VIEW V_CALENDAR AS
SELECT planned_date AS due_date, gate AS item, 'gate' AS item_type, scenario AS detail FROM GATES
UNION ALL
SELECT due_date, title AS item, kind AS item_type, status AS detail FROM TRACKED_ITEMS WHERE due_date IS NOT NULL;

-- Trend of tagged test results on main, one row per build.
CREATE OR REPLACE VIEW V_MAIN_TRENDS AS
SELECT build_id, MAX(generated_at) AS generated_at,
       COUNT(DISTINCT CASE WHEN kind = 'test' THEN test_id END)                                     AS tagged_tests,
       COUNT(DISTINCT CASE WHEN kind = 'test' AND result = 'pass' THEN test_id END)                 AS passing,
       COUNT(DISTINCT CASE WHEN kind = 'test' AND result IN ('fail', 'error') THEN test_id END)     AS failing
FROM EVIDENCE
WHERE branch = 'main' AND rule_key IS NOT NULL
GROUP BY build_id;

-- Time to restore (blameless): for each tagged test on main, each failure and when it passed again.
CREATE OR REPLACE VIEW V_TIME_TO_RESTORE AS
WITH runs AS (
  SELECT DISTINCT test_id, build_id, generated_at,
         CASE WHEN result IN ('fail', 'error') THEN 1 ELSE 0 END AS failed
  FROM EVIDENCE WHERE branch = 'main' AND kind = 'test' AND rule_key IS NOT NULL
),
marked AS (
  SELECT *, LAG(failed) OVER (PARTITION BY test_id ORDER BY generated_at) AS prev_failed FROM runs
),
starts AS (
  SELECT test_id, generated_at AS broke_at FROM marked WHERE failed = 1 AND COALESCE(prev_failed, 0) = 0
)
SELECT s.test_id, s.broke_at,
       (SELECT MIN(m.generated_at) FROM marked m
        WHERE m.test_id = s.test_id AND m.failed = 0 AND m.generated_at > s.broke_at) AS restored_at
FROM starts s;
