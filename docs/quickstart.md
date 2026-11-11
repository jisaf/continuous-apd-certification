# Vendor quickstart

Add continuous certification checks to an existing pipeline. Plan on about a day for the first useful
run: install, tag a first set of tests, add one pipeline step, and read the report.

## 1. Try it locally (15 minutes)

```sh
pip install "capd @ git+https://github.com/jisaf/continuous-apd-certification@v0.1.0"   # a release tag
capd catalog --search "standard deduction"      # find the rules your tests prove
```

From a checkout of this repository, `examples/sample-system/run-demo.sh` runs the whole flow on a sample
system, including a pull request with a simulated bug.

## 2. Tag the tests you already have

A tag names the rule a test proves. Use the rule key exactly as `capd catalog` prints it. Tag a feature
file or test class once to cover every test in it.

| Framework | How to tag | Report capd reads |
| --- | --- | --- |
| Gherkin (Cucumber, SpecFlow, Behave, pytest-bdd) | `@rule:fna:sirt:S0215` on a Feature or Scenario | Cucumber JSON |
| pytest | `@pytest.mark.rule("fna:sirt:S0215", "cms:ee:EE15")` (the plugin installs with capd) | JUnit XML with `-o junit_family=xunit1` |
| Playwright | `{ tag: '@rule:cms:ee:EE21' }` on a test or describe block, or `@rule:...` in the title | Playwright JSON (`--reporter=json`) |
| JUnit 5, Jest, others | A `<property name="rule" value="cms:ee:EE21"/>` on the test case in the JUnit XML | JUnit XML |
| .NET MSTest / VSTest | `[TestCategory("rule:cms:ee:EE21")]` with the [TRX connector](../examples/connector-template/) | TRX |
| Anything else | A sidecar file mapping test IDs (glob patterns) to rule keys (`sidecarTags` in `capd.yaml`) | Any of the above |

You never tag programs (Medicaid or SNAP): capd infers them from each rule. Pre-written, already-tagged
Gherkin templates for 588 SIRT rows and 26 CMS E&E outcomes are in [`examples/packs/`](../examples/packs/).

Run `capd check-tags` (or let `capd run` do it) to catch unknown keys and untagged tests in folders you
list under `taggedPaths`.

## 3. Add `capd.yaml`

Copy [`templates/config/capd.yaml`](../templates/config/capd.yaml) to the repository root. Point
`sources` at the reports your pipeline already writes, and keep `gateMode: report-only` to start.
The file is validated against [`config.schema.json`](../src/capd/data/schemas/config.schema.json).

## 4. Add one pipeline step

**Azure DevOps.** Copy [`templates/azure-devops/capd-steps.yml`](../templates/azure-devops/capd-steps.yml)
into your repository and add, after your tests:

```yaml
- template: templates/azure-devops/capd-steps.yml
  parameters:
    config: capd.yaml
```

Give the build service "Contribute to pull requests" on the repository so it can keep one sticky comment
thread. The step downloads the `capd-evidence` artifact from the latest successful build on main as the
baseline, so the first run on main creates it. A full example is
[`azure-pipelines.example.yml`](../templates/azure-devops/azure-pipelines.example.yml). To publish the
report to a private reports repository once a day, add
[`capd-publish-reports.yml`](../templates/azure-devops/capd-publish-reports.yml).

**GitHub Actions.** Copy [`templates/github-actions/capd.yml`](../templates/github-actions/capd.yml) to
`.github/workflows/` and call it after the job that uploads your test reports:

```yaml
certification:
  needs: tests
  if: always()
  uses: ./.github/workflows/capd.yml
  with: { config: capd.yaml, reports-artifact: test-reports }
  permissions: { contents: read, pull-requests: write, actions: read }
```

**Anything else.** Run the container or the CLI:

```sh
capd run --config capd.yaml --baseline path/to/main/bundle.json --out-dir out
docker run --rm -v "$PWD:/work" -w /work capd run --config capd.yaml
```

## 5. Read the results

Each run writes `out/report.html` (the [static report](reading-the-report.md)), `out/bundle.json` (the
evidence bundle; keep it as the next baseline), `out/comparison.json`, and `out/summary.md` (the pull
request comment).

## 6. Day-to-day rules

- **The gate only fails on regressions.** A tagged test that passed on main and fails now. Untagged tests
  never block. A failed test is rerun once and counts only if it fails again (configure your test runner's
  rerun; capd treats a test that passed on any attempt as passing).
- **Report-only first.** The state and the vendor agree, through a reviewed change to `gateMode`, when to
  switch to blocking.
- **Flaky tests go in `quarantine.txt`.** They still run and show in the report, but never block. Fix or
  remove each within two sprints.
- **Only pipeline data.** Do not point sources at Jira, production data, or security findings. Those join
  in the state's [report layer](report-layer.md).
- **No real case data** in tests, fixtures, or reports. Use synthetic data.

## Command reference

| Command | Does |
| --- | --- |
| `capd run` | collect → check-tags → compare → report → publish |
| `capd collect` | read reports into `bundle.json` |
| `capd check-tags` | lint tags (exit 1 on issues) |
| `capd compare` | the pull request gate (exit 1 only in blocking mode with a regression) |
| `capd report` | write the static HTML report |
| `capd publish` | run the sinks in `capd.yaml` (`--dry-run` shows what would be sent) |
| `capd validate orw FILE` / `intake FILE` | check an ORW or Intake Form against the pinned CMS template |
| `capd validate sirt FILE [--bundle B]` | check a SIRT response workbook: every row answered, a reason for each N, no moved rows; with a bundle, warn on Y answers whose tagged tests fail |
| `capd package check GATE DIR` | check a gate package folder and write a hashed submission record; see [gate packages](gate-packages.md) |
| `capd package verify RECORD [DIR]` | check that a submission record and its files have not changed |
| `capd validate templates` | check the pinned ORW template against CMS's ORW validation rules |
| `capd validate cases DIR` | check golden test cases against the schema |
| `capd catalog [--key K] [--search TEXT]` | browse the rules |
| `capd connectors` | list installed connectors |
