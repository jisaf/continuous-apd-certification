-- Snowflake: database, schemas, and the platform-specific BUNDLES table.
-- Then run ../sql/10_tables.sql, ../sql/20_metric_contract.sql (or your own contract views), and ../sql/30_views.sql
-- with USE SCHEMA CERTIFICATION.CERT. Finally run 20_roles.sql.
CREATE DATABASE IF NOT EXISTS CERTIFICATION;
CREATE SCHEMA IF NOT EXISTS CERTIFICATION.CERT;             -- pipeline evidence, tracked items, views
CREATE SCHEMA IF NOT EXISTS CERTIFICATION.CERT_RESTRICTED;  -- security findings: security role only
USE SCHEMA CERTIFICATION.CERT;

CREATE TABLE IF NOT EXISTS BUNDLES (
  build_id VARCHAR, commit_sha VARCHAR, branch VARCHAR, generated_at TIMESTAMP_NTZ,
  catalog_version VARCHAR, records_sha256 VARCHAR, bundle VARIANT
);

-- Restricted: security findings from the security team's tool (for example a POA&M export).
CREATE TABLE IF NOT EXISTS CERTIFICATION.CERT_RESTRICTED.SECURITY_FINDINGS (
  finding_id VARCHAR, source VARCHAR, severity VARCHAR, status VARCHAR,
  opened_at TIMESTAMP_NTZ, due_at TIMESTAMP_NTZ, rule_key VARCHAR, description VARCHAR
);
