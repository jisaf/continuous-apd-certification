# Research

## Classification (`classification/`)

Each item in four federal rule sets, classified by the evidence that best proves it. Done on 2026-11-11 by reading the text of every row. One reviewer did the classification and a 72-row spot check (72 of 72 primary types and 70 of 72 pre-write flags agreed), so the check is not independent. Treat the results as a working estimate.

| File | Rows | Source |
| --- | --- | --- |
| `ee_outcomes_classified.csv` | 27 CMS-required E&E outcomes | MES Certification Repository |
| `cef_classified.csv` | 22 Conditions for Enhanced Funding | MES Certification Repository |
| `sirt_classified.csv` | 917 rows: 821 SIRT item rows (`in_821=yes`) plus 96 related rows without an ID | FNA SNAP SIRT, Excel version |
| `golive_classified.csv` | 26 criteria | FNA SNAP Eligibility System Go Live Requirements (2023) |

Evidence types:

- `AUTO_TEST` — an automated functional test against the system
- `DATA_METRIC` — a count, percentage, or time from system or production data
- `REPORT_CHECK` — the system produces a specific report correctly
- `MANUAL_DEMO` — a human-run test, demonstration, or reviewer judgment
- `DOCUMENT` — a plan, policy, contract clause, letter, or attestation
- `EXTERNAL` — an outside party (PERM results, third-party security assessment, CMS-side data, interface partner sign-off)

For E&E outcomes, `orr_type` and `cr_type` give the evidence at the ORR (pre-production) and the CR (production). For SIRT rows, `prewrite_candidate` marks rows that a generic scenario plus a thin adapter could test.

### Summary

| Rule set | Items | Automated test | Data metric or report | Document | Outside party | Manual |
| --- | --- | --- | --- | --- | --- | --- |
| E&E outcomes at ORR | 27 | 26 | 0 | 0 | 0 | 1 |
| E&E outcomes at CR | 27 | 2 | 20 | 2 | 3 | 0 |
| CEF | 22 | 1 | 4 | 15 | 2 | 0 |
| SNAP SIRT | 821 | 638 | 87 | 71 | 1 | 24 |
| SNAP Go Live | 26 | 2 | 9 | 11 | 3 | 1 |

588 of the 821 SIRT rows are pre-write candidates.

## Notes (`notes/`)

- `hb901-and-sho25-003-notes.md` — verbatim notes on FNS Handbook 901 v2.5 chapters 1, 4, 5, 7, 9 and appendices, and on CMS SHO #25-003. Read the editor's note at the top: two of its conclusions were checked and rejected.
- `golden-case-sources.md` — published Medicaid and SNAP eligibility test cases that could seed the golden case set, with counts, licenses, and sample cases.
