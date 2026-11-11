-- Metric data contract: only the fields the tracked metrics read. Portable SQL (Snowflake and DuckDB).
-- In a state, these are usually VIEWS over the state's own tables, written from mapping.yaml.
-- For local runs and synthetic-data checks they are plain tables.

CREATE TABLE IF NOT EXISTS C_APPLICATION (
  application_id VARCHAR, received_at TIMESTAMP, channel VARCHAR,   -- online | phone | paper | in_person
  programs VARCHAR,                                                 -- comma list: medicaid,snap
  expedited BOOLEAN                                                 -- SNAP expedited service screening result
);
CREATE TABLE IF NOT EXISTS C_DETERMINATION (
  application_id VARCHAR, program VARCHAR, result VARCHAR,          -- approved | denied
  decided_at TIMESTAMP, automated BOOLEAN,                          -- no manual touch
  method VARCHAR                                                    -- MAGI | non-MAGI | SNAP
);
CREATE TABLE IF NOT EXISTS C_NOTICE (
  notice_id VARCHAR, application_id VARCHAR, notice_type VARCHAR, channel VARCHAR,
  generated_at TIMESTAMP, sent_at TIMESTAMP, automatic BOOLEAN
);
CREATE TABLE IF NOT EXISTS C_RENEWAL (
  renewal_id VARCHAR, program VARCHAR, due_date DATE, completed_at TIMESTAMP,
  ex_parte BOOLEAN, prepopulated_sent BOOLEAN
);
CREATE TABLE IF NOT EXISTS C_WORK_ITEM (
  item_id VARCHAR, item_type VARCHAR, created_at TIMESTAMP, status VARCHAR, due_date DATE
);
CREATE TABLE IF NOT EXISTS C_APPEAL_TRANSFER (
  record_id VARCHAR, record_type VARCHAR,                           -- appeal | account_transfer
  channel VARCHAR, received_at TIMESTAMP, completed_at TIMESTAMP, status VARCHAR
);
