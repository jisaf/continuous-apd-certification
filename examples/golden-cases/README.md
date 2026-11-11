# Golden test cases

Household facts in, expected outcome out, in the framework-neutral format defined by
[`test-case.schema.json`](../../src/capd/data/schemas/test-case.schema.json). Check them with
`capd validate cases examples/golden-cases`.

| Folder | Cases | Source | License |
| --- | --- | --- | --- |
| [`snap/`](snap/) | 37 | 18F SNAP API prototype scenarios (IL, UT, VT), converted by [`tools/import_18f_cases.py`](../../tools/import_18f_cases.py) | CC0 (U.S. government work) |

**These are historical samples.** The expected values are 18F's FY2020 results for the named states. They
show the format and exercise the sample system. A state's policy staff must recompute expected values for
the state's own rules and the current fiscal year (SNAP rules changed in 2025).

Each case lists the rule keys it proves. A vendor or the state can **dispute** a case by setting
`status: disputed` with a `dispute` note; disputed cases are excluded from pass rates until resolved.

Other sources researched, with their licenses and how each may be used, are in
[`docs/research/notes/golden-case-sources.md`](../../docs/research/notes/golden-case-sources.md).
