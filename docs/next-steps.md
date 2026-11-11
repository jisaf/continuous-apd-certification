# Next steps

Status as of 2026-11-11. The full reasoning is in [`proposal.md`](proposal.md).

## Phase 0 — Foundation (useful on its own)

1. **Rules catalog, version 0.**
   - Extract the CMS-required E&E outcomes and the 22 CEFs from the [MES Certification Repository](https://github.com/CMSgov/CMCS-DSG-DSS-Certification), pinned to a reviewed commit.
   - Extract the SNAP SIRT from FNA's Excel version, the SNAP Go Live Requirements, and the FNA testing gates from Handbook 901.
   - Give every item a stable catalog key, because agency IDs repeat (524 unique SIRT IDs cover 821 rows).
   - Record for each item: source and citation, gates, evidence type (from [`research/classification/`](research/classification/)), and whether it is a leading indicator.
2. **Schemas.** JSON Schemas for catalog entries, the evidence record, the evidence bundle, state configuration (`mapping.yaml`), the connector interface, the metric data contract, and the test case format.
3. **File validators** for the agencies' current templates: the new CMS templates from SHO #25-003 (SMC Intake Form, Operational Report Workbook) and the FNA SIRT response workbook.
4. **Static report generator.** One self-contained HTML file per build, built from the pipeline's evidence bundle alone. It never reads external data (Jira, production data, security findings, documents).
5. **Two small contracts, not a data model.** The metric data contract (six record types: Application, Determination, Notice, Renewal, Work item, Appeal and account transfer — only the fields the metrics read) and the test case format (household facts in, expected outcome out).

## Phase 1 — Build to ORR (first state project)

- Pipeline connectors: GitHub, Azure DevOps (pipeline step and summary), Jira (one issue per rule or gate out), email and chat digests.
- Report layer on the state's existing data platform (first adaptation: Snowflake), mostly patterns and templates in portable SQL: certification schema, evidence load pattern, metric query templates, role and secure-view templates, starter dashboards, and loaders for external data (Jira defects, security findings).
- Example test packs: SIRT pre-write candidates and the E&E outcomes with clear behaviour, as Gherkin with rule IDs tagged.
- Golden case set for the policy indicators (see below).
- Package generators for the ORR and the FNA UAT Go/No-Go.
- APD watch rules (gate forecasts against the approved APD baseline).

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
