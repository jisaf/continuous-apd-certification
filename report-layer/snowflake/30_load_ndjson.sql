-- Alternative to the snowflake sink: load the file sink's evidence-rows.ndjson from a stage.
USE SCHEMA CERTIFICATION.CERT;
CREATE FILE FORMAT IF NOT EXISTS CAPD_NDJSON TYPE = JSON;
CREATE STAGE IF NOT EXISTS CAPD_STAGE FILE_FORMAT = CAPD_NDJSON;
-- From the pipeline:  PUT file://out/evidence-rows.ndjson @CAPD_STAGE/<build_id>/ ;
COPY INTO EVIDENCE (build_id, commit_sha, branch, generated_at, catalog_version, rule_key, kind, result, value, unit,
                    programs, environment, executed_by, test_id, name, observed_at, source_uri)
FROM (SELECT $1:build_id, $1:commit_sha, $1:branch, $1:generated_at, $1:catalog_version, $1:rule_key, $1:kind,
             $1:result, $1:value, $1:unit, $1:programs, $1:environment, $1:executed_by, $1:test_id, $1:name,
             $1:observed_at, $1:source_uri
      FROM @CAPD_STAGE)
ON_ERROR = ABORT_STATEMENT;
