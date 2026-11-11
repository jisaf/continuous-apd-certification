# Next steps

Status as of 2026-11-11. The full reasoning is in [`proposal.md`](proposal.md).

## Phase 0 — Foundation (useful on its own)

1. **Rules catalog, version 0.**
   - Extract the CMS-required E&E outcomes and the 22 CEFs from the [MES Certification Repository](https://github.com/CMSgov/CMCS-DSG-DSS-Certification), pinned to a reviewed commit.
   - Extract the SNAP SIRT from FNA's Excel version, the SNAP Go Live Requirements, and the FNA testing gates from Handbook 901.
   - Give every item a stable catalog key, because agency IDs repeat (524 unique SIRT IDs cover 821 rows).
   - Record for each item: source and citation, gates, evidence type (from [`research/classification/`](research/classification/)), evidence class (open, summary only, restricted, aggregate only), and whether it is a leading indicator.
2. **Schemas.** JSON Schemas for catalog entries, the evidence record, the evidence bundle, state configuration (`mapping.yaml`), and the connector interface.
3. **File validators** for the agencies' current templates: the new CMS templates from SHO #25-003 (SMC Intake Form, Operational Report Workbook) and the FNA SIRT response workbook.
4. **Static report generator.** One self-contained HTML file per build from an evidence bundle. It renders only the open and summary-only evidence classes; this is enforced in code and tested.
5. **Reference entities, first four.** Application, Eligibility determination, Notice, Renewal — with reference metric queries for the default E&E metrics and the Go Live numbers.

## Phase 1 — Build to ORR (first state project)

- Connectors: GitHub, Azure DevOps (pipeline step and summary), Jira (defects in; one issue per rule or gate out), Snowflake (metric queries in; evidence tables out), email and chat digests.
- Example test packs: SIRT pre-write candidates and the E&E outcomes with clear behaviour, as Gherkin with rule IDs tagged.
- Golden case set for the policy indicators (see below).
- Package generators for the ORR and the FNA UAT Go/No-Go.
- APD watch rules (gate forecasts against the approved APD baseline).

## Decisions still needed

- Which evidence classes each state role may see, and the exact restricted list.
- Legal review of the [contributor license agreement](../CLA.md).
- Confirmation from FNA and CMS that generated files in their templates, and the reading of the pilot rule, are acceptable.

## Golden case set

Sources were researched on 2026-11-11 ([notes](research/notes/golden-case-sources.md)). Plan:

1. Ask the state Medicaid agency for the 100 CMS PERM eligibility review test cases and the state's answer key, and for any regression test decks from its current eligibility system.
2. Copy the 145 18F SNAP scenarios (U.S. government work, CC0) and the CMS MAGI worked examples into the CC0 set, and recompute every expected value for the target state and the current fiscal year.
3. Adapt scenarios from the state's published renewal workbooks and desk aids, with citations.
4. Use PolicyEngine US (AGPL-3.0) and MAGI in the Cloud (BSD-3) as independent engines to cross-check cases, without copying their cases into the CC0 set.
5. Use the USDA SNAP QC public use file for statistical regression on the target state's households.
6. Write new cases only for the gaps: expedited service, ABAWD month counting, notices, SNAP recertification, combined Medicaid and SNAP households, and state options.
