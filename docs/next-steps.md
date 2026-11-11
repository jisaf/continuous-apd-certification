# Next steps

Status as of 2026-11-11. The full reasoning is in [`proposal.md`](proposal.md).

**MVP built (2026-11-11):** the rules catalog, schemas, CLI, source and sink connectors, conformance kit, static report, ORW and Intake Form validators, mapping-to-views, pre-written packs, golden cases, sample system, pipeline templates, and the report layer (portable SQL, Snowflake setup, DuckDB builder, dashboard). Phase 0 items 1–6 below are done in a first version; the rest of this list is what follows.

## Phase 0 — Foundation (useful on its own)

1. **Rules catalog, version 0.**
   - Extract the CMS-required E&E outcomes and the 22 CEFs from the [MES Certification Repository](https://github.com/CMSgov/CMCS-DSG-DSS-Certification), pinned to a reviewed commit.
   - Extract the SNAP SIRT from FNA's Excel version, the SNAP Go Live Requirements, and the FNA testing gates from Handbook 901.
   - Give every item a stable catalog key, because agency IDs repeat (524 unique SIRT IDs cover 821 rows).
   - Record for each item: source and citation, gates, evidence type (from [`research/classification/`](research/classification/)), whether it is a leading indicator, responsibility (vendor, state, third party, shared), coverage (evidenced, tracked only, not covered), and whether state acceptance is required.
   - Record the source that is authoritative for each rule, and flag stale references (for example, the CMS repository's Planning page still cites MARS-E, which ARC-AMPE replaced).
2. **Integration contract v1, released before any solicitation relies on it.** JSON Schemas for catalog entries, the evidence record, the evidence bundle, state configuration (`mapping.yaml`), the connector interface, the metric data contract, and the test case format; one rule key syntax (`agency:set:id`) with permanent SIRT keys; tag conventions per test framework; a `check-tags` lint; reference Azure DevOps and GitHub Actions pipeline files; a one-day quickstart.
3. **File validators** for the agencies' current templates: the new CMS templates from SHO #25-003 (SMC Intake Form, Operational Report Workbook) and the FNA SIRT response workbook.
4. **Rule-status logic and one calendar for both agencies.** Publish the status definitions (N/A, No evidence, Not met, Stale, At risk, Met) and the combined CMS and FNA calendar, with gate order, APD update triggers for both agencies, ARC-AMPE timelines, and disaster recovery tests as configuration.
5. **Static report generator.** One self-contained HTML file per build, built from the pipeline's evidence bundle alone. It never reads external data (Jira, production data, security findings, documents).
6. **Two small contracts, not a data model.** The metric data contract (six record types: Application, Determination, Notice, Renewal, Work item, Appeal and account transfer — only the fields the metrics read) and the test case format (household facts in, expected outcome out).

## Phase 1 — Build to ORR (first state project)

- Pull request gate: fail only when a tagged test that passed on main now fails; report-only by default; flaky-test quarantine; one comment updated in place.
- Pipeline connectors: GitHub, Azure DevOps (pipeline step and summary), Jira (one issue per gate, plus blocker issues that close themselves), email and chat digests sent only on status changes.
- Report layer on the state's existing data platform (first adaptation: Snowflake), mostly patterns and templates in portable SQL: certification schema, evidence load pattern, metric query templates, role and secure-view templates, starter dashboards, and loaders for external data (Jira defects, security findings).
- Example test packs: SIRT pre-write candidates and the E&E outcomes with clear behaviour, as Gherkin with rule IDs tagged.
- Golden case set for the policy indicators (see below).
- Gate package checklists, template-version detection, and a hashed submission record: built (`capd package`, `capd validate sirt`; see [gate packages](gate-packages.md)).
- APD watch rules: dropped. Scope is technical readiness; APD and cost allocation are tracked as dates only.

## Optional phase 2

- Inferred rule tags from a Jira epic-to-outcome map. Not part of the core product. (Program tags are inferred in the core from each rule's agency.)

## Solicitation support

- Recommended QASP additions for a time-and-materials order: certification-specific measures that add to the state's existing QASP, and an artifact ownership table.

## Decisions still needed

- Which report layer roles see which external data, starting from the role templates.
- Confirmation from FNA and CMS that generated files in their templates, and the reading of the pilot rule, are acceptable.

## Golden case set

Sources were researched on 2026-11-11 ([notes](research/notes/golden-case-sources.md)). Plan:

1. Ask the state Medicaid agency for the 100 CMS PERM eligibility review test cases and the state's answer key, and for any regression test decks from its current eligibility system.
2. Copy the 145 18F SNAP scenarios (U.S. government work, CC0) and the CMS MAGI worked examples into the CC0 set, and recompute every expected value for the target state and the current fiscal year.
3. Adapt scenarios from the state's published renewal workbooks and desk aids, with citations.
4. Use PolicyEngine US (AGPL-3.0) and MAGI in the Cloud (BSD-3) as independent engines to cross-check cases, without copying their cases into the CC0 set.
5. Use the USDA SNAP QC public use file for statistical regression on the target state's households.
6. Write new cases only for the gaps: expedited service, ABAWD month counting, notices, SNAP recertification, combined Medicaid and SNAP households, and state options.
