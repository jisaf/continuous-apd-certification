-- DuckDB-specific table: the raw bundle JSON. Portable tables are in ../sql/10_tables.sql.
CREATE TABLE IF NOT EXISTS BUNDLES (
  build_id VARCHAR, commit_sha VARCHAR, branch VARCHAR, generated_at TIMESTAMP,
  catalog_version VARCHAR, records_sha256 VARCHAR, bundle JSON
);
