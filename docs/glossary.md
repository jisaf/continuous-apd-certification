# Glossary

| Term | Meaning here |
| --- | --- |
| **Rule** | One certification requirement from a federal source: a CMS E&E outcome, a Condition for Enhanced Funding (CEF), a SNAP System Integrity Review Tool (SIRT) row, or a SNAP Go Live criterion. States can add their own. |
| **Rule key** | The stable identifier of a rule, `<agency>:<set>:<id>`, for example `cms:ee:EE21`, `cms:cef:CEF12`, `fna:sirt:S0215`, `fna:golive:GL03`, `state:ee:STEE01`. Keys never change or get reused. |
| **capd** | The name of the Python package and command-line tool, short for "continuous APD". |
| **Catalog** | The versioned list of all rules (`src/capd/data/catalog/catalog.json`). A project pins one version; updates go through change control. |
| **Gate** | A federal review point: `ORR` (CMS Operational Readiness Review), `CR` (CMS Certification Review), `FNA-UAT` (FNA UAT Go/No-Go), `FNA-PILOT` (FNA pilot Go/No-Go). |
| **Evidence kind** | What proves a rule at a gate: `test`, `scan`, `metric`, `report`, `document`, `attestation`, `demonstration`, or `assessment`. |
| **Tag** | A rule key attached to a test, so the test's result becomes evidence for that rule. |
| **Evidence record** | One result: a test, scan, or metric, with its rule keys, result, build, commit, and time. |
| **Evidence bundle** | All evidence records from one pipeline run, with a hash that detects later changes. |
| **Baseline** | The evidence bundle from the last build on main. Pull requests are compared with it. |
| **Regression** | A tagged test or scan that passed on main and fails now. The only thing the gate can block on. |
| **Report-only / blocking** | The gate's two modes. Report-only comments but never fails a build. Blocking fails a build on a regression. |
| **Quarantine** | A list of flaky tests that still run but never block. Each should be fixed or removed within two sprints. |
| **Static report** | The self-contained HTML file each run writes. Pipeline data only. |
| **Report layer** | Optional tables, views, and dashboards on the state's existing data platform, where pipeline evidence joins external data (tracked items, acceptances, production metrics, defects). Mostly templates. |
| **Tracked item** | External evidence the state tracks where it already lives: a letter, plan, assessment, demonstration, or an APD date. Tracked by status and date, not modeled. |
| **Rule status** | Decided in the report layer, per rule and gate: N/A, Disputed, No evidence, Not met, Stale, At risk, Awaiting acceptance, Met. |
| **Met** | The toolkit's readiness signal that a rule's required evidence is present, passing, fresh, and (where required) accepted by the state. Not CMS's "Evidence Satisfactory" or FNA's concurrence. |
| **Blocker** | A rule or tracked item that stands in the way of a gate: No evidence, Not met, Stale, Disputed, At risk, or overdue. Shown as a list, never a percentage. |
| **Golden case** | A test case with household facts in and the expected outcome out, owned by state policy staff. |
| **System adapter** | The small piece of vendor code that turns a golden case or example test into a call to its system. |
| **Connector** | A plugin that reads evidence (source) or publishes results (sink). |
| **Metric data contract** | The few fields the metric queries read, in six record types. States map their own tables to it. |
| **Coverage** | How far the toolkit covers a rule: *evidenced* (it produces or checks the evidence), *tracked only*, or *not covered*. |
| **Responsibility** | Who is responsible for a rule's evidence: vendor, state, third party, or shared. |
