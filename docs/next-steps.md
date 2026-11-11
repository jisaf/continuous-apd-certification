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

## Phase 1 — Build to ORR (Colorado)

- Connectors: GitHub, Azure DevOps (pipeline step and summary), Jira (defects in; one issue per rule or gate out), Snowflake (metric queries in; evidence tables out), email and chat digests.
- Example test packs: SIRT pre-write candidates and the E&E outcomes with clear behaviour, as Gherkin with rule IDs tagged.
- Golden case set for the policy indicators (seeded from published sources — research in progress).
- Package generators for the ORR and the FNA UAT Go/No-Go.
- APD watch rules (gate forecasts against the approved APD baseline).

## Decisions still needed

- Which evidence classes each Colorado role may see, and the exact restricted list.
- Legal review of the [contributor license agreement](../CLA.md).
- Confirmation from FNA and CMS that generated files in their templates, and the reading of the pilot rule, are acceptable.

## Research in progress

- Published Medicaid and SNAP eligibility test cases (households with known expected outcomes) to seed the golden case set, rather than inventing new ones.
