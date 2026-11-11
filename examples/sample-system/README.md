# Sample system: an end-to-end demo of the pipeline

This folder plays the part of a state's eligibility system so you can run the whole toolkit locally.

- **The "system":** `vendor/snap_financial_factors`, the 18F SNAP API prototype's benefit calculator
  (U.S. government work, CC0; see `vendor/LICENSE-18F.md`). Its determination API takes a household and
  returns eligibility and a monthly benefit. It uses FY2020 federal parameters.
- **The system adapter:** `adapter.py` turns a golden test case (household facts in, expected outcome out)
  into a call to that API. In a real project, this is the one piece the vendor writes for its own system.
- **Tagged tests, two styles:**
  - `tests/test_golden_cases.py` runs every case in `../golden-cases/snap/` with pytest. Each case's rule
    keys become `@pytest.mark.rule(...)` marks, written to JUnit XML by the capd pytest plugin.
  - `features/standard_deduction.feature` is Gherkin with `@rule:` tags, run by pytest-bdd, which writes
    Cucumber JSON.
- **A security scan:** ruff's security rules (`S`) over `adapter.py`, written as SARIF.
- **Configuration:** `capd.yaml`, `quarantine.txt`, and `sidecar-tags.yaml`.

## Run it

From the repository root, after `pip install -e ".[dev]"`:

```sh
examples/sample-system/run-demo.sh
```

The script runs the tests and `capd run` twice:

1. A clean "main" build, saved as the baseline.
2. A "pull request" build with a simulated bug (`CAPD_DEMO_BUG=standard-deduction` makes the system
   ignore the standard deduction). The pull request gate reports the regressions against main.

Open `out/demo/pr/report.html` to read the static report. The same files a pipeline would publish are
in `out/demo/pr/`: `bundle.json`, `comparison.json`, `summary.md` (the pull request comment), and
`evidence-rows.ndjson` (for the report layer).
