# Contributing

This project is in the planning stage. The most useful contributions right now are:

- **Corrections** to how we read CMS and FNA requirements, with a citation to the source.
- **Experience** from states, vendors, IV&V teams, or federal reviewers: what slowed your last ORR, CR, UAT Go/No-Go, or pilot.
- **Pointers to published test cases** for Medicaid and SNAP eligibility (see [`docs/next-steps.md`](docs/next-steps.md)).

Open a GitHub issue for any of these.

## Ground rules

- **Never include real case data.** No applicant or recipient names, identifiers, case numbers, screenshots of real cases, or protected health information — in issues, pull requests, test data, or examples. Use synthetic data only.
- **Never include security findings** about any real system.
- **Cite sources.** For any rule, give the document, section, and a link.

## Code contributions

Outside code contributions need a signed [contributor license agreement](CLA.md). The agreement is a draft under legal review, so outside code cannot be merged yet. Documentation and research fixes under CC0 are welcome now.

When code exists, every change will need:

- tests;
- for connectors, a passing run of the shared connector conformance suite;
- for rules, a citation to the CMS or FNA source.
