# The report layer

The report layer is where pipeline evidence meets everything the pipeline cannot see: the state's tracked
items (letters, plans, assessments, demonstrations), acceptance decisions, production metrics, gate dates,
and defects. It decides each rule's status for each gate and lists gate blockers.

It is **optional and mostly templates**. It runs on the data platform and BI tool the state already has, so
it needs no new hosting. The SQL is portable: the same files run on Snowflake and on DuckDB.

| Piece | Files |
| --- | --- |
| Tables | [`sql/10_tables.sql`](../report-layer/sql/10_tables.sql): `RULES`, `RULE_GATES`, `EVIDENCE`, `TRACKED_ITEMS`, `ACCEPTANCES`, `GATES`, `DEFECTS` |
| Metric data contract | [`sql/20_metric_contract.sql`](../report-layer/sql/20_metric_contract.sql): six record types, only the fields the metrics read |
| Views | [`sql/30_views.sql`](../report-layer/sql/30_views.sql): `V_RULE_STATUS`, `V_GATE_BLOCKERS`, `V_CALENDAR`, `V_MAIN_TRENDS`, `V_TIME_TO_RESTORE` |
| Metric queries | [`sql/metrics/`](../report-layer/sql/metrics/): EE5, EE6, EE9, EE13, SNAP timeliness, backlog |
| Snowflake | [`snowflake/`](../report-layer/snowflake/): schemas, roles and secure views, NDJSON load, catalog load |
| DuckDB (local) | [`duckdb/build_local.py`](../report-layer/duckdb/build_local.py) |
| Dashboard | [`dashboard/app.py`](../report-layer/dashboard/app.py) (Streamlit) and [`dashboard/queries.py`](../report-layer/dashboard/queries.py) |
| Sample state data | [`sample-data/`](../report-layer/sample-data/): gates, tracked items, acceptances, defects |

## Try it locally in five minutes (DuckDB)

```sh
pip install -e ".[dev]"                                    # from the repository root
examples/sample-system/run-demo.sh                         # produces pipeline evidence
python report-layer/duckdb/build_local.py                  # builds out/report-layer/cert.duckdb
pip install streamlit
streamlit run report-layer/dashboard/app.py -- --duckdb out/report-layer/cert.duckdb
```

`build_local.py` loads the catalog, every `evidence-rows.ndjson` it finds, the sample state data, and
synthetic metric data, then runs the metric queries into `out/report-layer/metrics/`.

## Set it up on Snowflake

1. **Schemas.** Run [`snowflake/10_schema.sql`](../report-layer/snowflake/10_schema.sql). It creates the
   `CERTIFICATION` database, the `CERT` schema, the restricted `CERT_RESTRICTED` schema, and the `BUNDLES` table.
2. **Tables and views.** With `USE SCHEMA CERTIFICATION.CERT;`, run `sql/10_tables.sql`, then either
   `sql/20_metric_contract.sql` (tables, for synthetic data) or your own views with the same names over your
   tables, then `sql/30_views.sql`.
3. **Roles.** Run [`snowflake/20_roles.sql`](../report-layer/snowflake/20_roles.sql). Map the roles to state
   groups through single sign-on:

   | Role | Who | Can |
   | --- | --- | --- |
   | `CERT_VIEWER` | Director, project manager, vendor | Read views; security findings only as counts (`V_SECURITY_SUMMARY`) |
   | `CERT_ACCEPTOR` | State product owner | Also record acceptance decisions |
   | `CERT_SECURITY` | State security officer | Read and write the restricted security findings |
   | `CERT_LOADER` | Pipeline service identity | Write pipeline evidence only |

4. **Catalog.** Upload `catalog.json` from the installed capd package to the stage and run
   [`snowflake/40_load_catalog.sql`](../report-layer/snowflake/40_load_catalog.sql).
5. **Evidence.** Either add the `snowflake` sink to `capd.yaml` (`pip install "capd[snowflake]"`, key-pair
   credentials for `CERT_LOADER` as pipeline secrets), or stage the file sink's `evidence-rows.ndjson` and
   run [`snowflake/30_load_ndjson.sql`](../report-layer/snowflake/30_load_ndjson.sql).
6. **Dashboard.** Create a Streamlit in Snowflake app from `dashboard/app.py` and `dashboard/queries.py` in
   the `CERT` schema. Viewers sign in with their own identity, so Snowflake roles apply.

## Load the state's own data

These come from where they already live. Load them on whatever schedule suits the state.

| Table | From | Notes |
| --- | --- | --- |
| `GATES` | The project schedule | Planned date per gate, and the agreed gate-order scenario |
| `TRACKED_ITEMS` | The state's document store, security tool, APD office | Letters, plans, assessments, demonstrations, APD and cost allocation dates. Status and date only. Set `rule_key` when the item is evidence for a catalog rule |
| `ACCEPTANCES` | The state product owner | `accepted`, `rejected`, `disputed`, `dispute_resolved`, `na_accepted` |
| `DEFECTS` | Jira or Azure Boards export | Key, severity, status, dates, rule keys. No free text |
| `CERT_RESTRICTED.SECURITY_FINDINGS` | The security team's tool (for example a POA&M export) | Security role only; viewers see counts |
| Metric contract views | The state's warehouse | Map with views; see `mapping.yaml` in [`templates/config/`](../templates/config/) and the [proposal](proposal.md) |

## Other BI tools

Power BI and Tableau connect to the same views. Use each person's own identity (single sign-on) so the
platform's roles apply; do not use a shared viewing account. The queries in
[`dashboard/queries.py`](../report-layer/dashboard/queries.py) are plain SQL you can paste as custom queries.

## Rules the views follow

- **Status order:** N/A, Disputed, No evidence, Not met, Stale, At risk, Awaiting acceptance, Met. The same
  logic is in Python ([`capd/status.py`](../src/capd/status.py)), and the test suite checks they agree.
- **Met is a readiness signal,** not CMS's "Evidence Satisfactory" or FNA's concurrence.
- **Blockers are a list, never a percentage.**
- **Environment matters only for metrics:** production data for the CR, pilot data for the pilot.
- **Only evidence that is produced once can be "At risk"** before a far-off gate; tests and metrics refresh.
- **Counts under 11** from case data are suppressed (`SUPPRESS_SMALL` in the Snowflake template).
