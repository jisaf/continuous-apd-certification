-- Load the capd catalog into RULES and RULE_GATES. Upload catalog.json (from the capd package:
-- python -c "import capd, os; print(os.path.dirname(capd.__file__) + '/data/catalog/catalog.json')") to the stage first:
--   PUT file://catalog.json @CAPD_STAGE/catalog/ ;
USE SCHEMA CERTIFICATION.CERT;
CREATE OR REPLACE TEMPORARY TABLE CATALOG_RAW AS
SELECT $1 AS doc FROM @CAPD_STAGE/catalog/catalog.json (FILE_FORMAT => 'CAPD_NDJSON');
DELETE FROM RULES;
INSERT INTO RULES
SELECT r.value:key::VARCHAR, r.value:agency::VARCHAR, r.value:set::VARCHAR, r.value:sourceId::VARCHAR, r.value:title::VARCHAR,
       r.value:responsibility::VARCHAR, r.value:coverage::VARCHAR, r.value:acceptance::VARCHAR, r.value:freshnessDays::INTEGER,
       ARRAY_TO_STRING(r.value:programs, ','), COALESCE(r.value:applicable::BOOLEAN, TRUE)
FROM CATALOG_RAW, LATERAL FLATTEN(input => doc:rules) r;
DELETE FROM RULE_GATES;
INSERT INTO RULE_GATES
SELECT r.value:key::VARCHAR, g.key::VARCHAR, k.value::VARCHAR
FROM CATALOG_RAW, LATERAL FLATTEN(input => doc:rules) r, LATERAL FLATTEN(input => r.value:gates) g, LATERAL FLATTEN(input => g.value) k;
