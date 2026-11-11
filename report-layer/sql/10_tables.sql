-- Report layer tables (portable SQL: runs on Snowflake and DuckDB).
-- Run after selecting the target schema, for example: USE SCHEMA CERTIFICATION.CERT;
-- BUNDLES (raw JSON) is platform-specific: see snowflake/10_schema.sql or duckdb/10_schema.sql.

-- The rules catalog, loaded from capd's catalog.json (see load scripts).
CREATE TABLE IF NOT EXISTS RULES (
  rule_key        VARCHAR PRIMARY KEY,
  agency          VARCHAR,
  rule_set        VARCHAR,
  source_id       VARCHAR,
  title           VARCHAR,
  responsibility  VARCHAR,   -- vendor | state | third_party | shared
  coverage        VARCHAR,   -- evidenced | tracked_only | not_covered
  acceptance      VARCHAR,   -- required | not_required
  freshness_days  INTEGER,
  programs        VARCHAR,
  applicable      BOOLEAN
);

-- Evidence kinds each rule needs at each gate.
CREATE TABLE IF NOT EXISTS RULE_GATES (
  rule_key  VARCHAR,
  gate      VARCHAR,   -- ORR | CR | FNA-UAT | FNA-PILOT
  kind      VARCHAR    -- test | metric | report | document | attestation | demonstration | assessment
);

-- One row per (evidence record, rule key) from each pipeline run: the file sink's evidence-rows.ndjson
-- or the snowflake sink. Pipeline-produced data only.
CREATE TABLE IF NOT EXISTS EVIDENCE (
  build_id         VARCHAR,
  commit_sha       VARCHAR,
  branch           VARCHAR,
  generated_at     TIMESTAMP,
  catalog_version  VARCHAR,
  rule_key         VARCHAR,
  kind             VARCHAR,
  result           VARCHAR,
  value            DOUBLE,
  unit             VARCHAR,
  programs         VARCHAR,
  environment      VARCHAR,
  executed_by      VARCHAR,
  test_id          VARCHAR,
  name             VARCHAR,
  observed_at      TIMESTAMP,
  source_uri       VARCHAR
);

-- External evidence the state tracks where it already lives: letters, plans, demonstrations,
-- third-party assessments, APD submissions, cost allocation approval. Tracked by status and date, not modeled.
CREATE TABLE IF NOT EXISTS TRACKED_ITEMS (
  item_key     VARCHAR,
  rule_key     VARCHAR,        -- may be NULL for items that are not catalog rules (for example an APD Update)
  gate         VARCHAR,
  kind         VARCHAR,        -- document | attestation | demonstration | assessment | external
  title        VARCHAR,
  owner        VARCHAR,
  due_date     DATE,
  status       VARCHAR,        -- open | submitted | complete
  result       VARCHAR,        -- present | pass | fail
  observed_at  TIMESTAMP,      -- when the evidence was produced or last refreshed
  link         VARCHAR,
  source       VARCHAR
);

-- State acceptance, disputes, and accepted N/A justifications. Latest decision per rule and gate wins.
CREATE TABLE IF NOT EXISTS ACCEPTANCES (
  rule_key    VARCHAR,
  gate        VARCHAR,
  decision    VARCHAR,   -- accepted | rejected | disputed | dispute_resolved | na_accepted
  role        VARCHAR,
  decided_at  TIMESTAMP,
  note        VARCHAR
);

-- Planned gate dates and the agreed gate-order scenario.
CREATE TABLE IF NOT EXISTS GATES (
  gate          VARCHAR,
  planned_date  DATE,
  scenario      VARCHAR
);

-- Defects exported from the tracker (summary fields only: no free text).
CREATE TABLE IF NOT EXISTS DEFECTS (
  defect_key  VARCHAR,
  severity    VARCHAR,
  status      VARCHAR,
  opened_at   TIMESTAMP,
  closed_at   TIMESTAMP,
  rule_keys   VARCHAR
);
