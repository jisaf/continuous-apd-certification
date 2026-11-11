# For states

**What you get:** a running, honest view of how close your eligibility system is to CMS certification and
FNA approval, built from the vendor's everyday work, without a new system to host or a separate security
review.

## The problem it solves

CMS and FNA reviews come at fixed points: FNA's test plan and Go/No-Go decisions, CMS's Operational
Readiness Review (ORR) and Certification Review (CR). Today the evidence is usually assembled by hand in the
weeks before each review, so problems surface late, when they cost the most. Most of that evidence (test
results, defects, scans, metrics) already exists inside the vendor's pipeline every day.

## What changes for you

| Today | With continuous certification |
| --- | --- |
| Readiness is a status-report opinion | Every build shows which rules have passing tests, and a pull request that breaks one is flagged |
| Evidence is gathered before each review | Evidence accumulates continuously, with a hashed record of each run |
| A green percentage hides a missing letter | Gate blockers are a list, never a percentage |
| CMS and FNA tracks are separate | One catalog and one calendar cover both agencies, including their different update triggers |
| Accountability debates are personal | Reports name rules and tests, never people; measures use time to restore |

## See it before you decide

Every sample below is in this repository and works today.

| Sample | What it shows | Where |
| --- | --- | --- |
| Static report, pull request build | What your team sees on every pull request: tagged results, regressions against main, coverage by rule set | [`sample-report/pull-request-build.html`](sample-report/pull-request-build.html) |
| Static report, main build | The daily view of the main branch | [`sample-report/main-build.html`](sample-report/main-build.html) |
| Pull request comment | The one comment the pipeline keeps up to date on each change | [`sample-report/pull-request-comment.md`](sample-report/pull-request-comment.md) |
| Five-minute demo | A sample system, a clean build, then a change with a simulated bug that the check catches | [README](../README.md#see-it-in-five-minutes) and [`examples/sample-system/`](../examples/sample-system/) |
| Dashboard with sample state data | Gate blockers, rule status, calendar, trends, time to restore | [`report-layer/`](../report-layer/) and [the report layer guide](report-layer.md) |
| Sample state data | Gate dates, tracked items (letters, plans, assessments), acceptance decisions, defects | [`report-layer/sample-data/`](../report-layer/sample-data/) |
| Golden test cases | Household facts in, expected outcome out, ready for your policy staff to adapt | [`examples/golden-cases/`](../examples/golden-cases/) |
| Pre-written test templates | 588 SNAP SIRT scenarios and 26 CMS E&E features, already tagged with rule keys | [`examples/packs/`](../examples/packs/) |
| Project configuration | Every option, commented | [`templates/config/capd.yaml`](../templates/config/capd.yaml) |
| Mapping to your data | How your tables feed the federal metrics | [`templates/config/mapping.yaml`](../templates/config/mapping.yaml) |
| Pipeline templates | Azure DevOps and GitHub Actions | [`templates/`](../templates/) |

## How you see it

1. **Static report per build** (no hosting). The vendor's pipeline publishes it to a private reports
   repository once a day. It shows only pipeline data. See [how to read it](reading-the-report.md).
2. **Pull request comments, Jira gate issues, chat digests** in the tools your team already uses.
3. **The report layer and dashboard** (optional) on your existing data platform, for example Snowflake.
   Pipeline evidence joins your tracked items, acceptance decisions, production metrics, and gate dates to
   give each rule a status and list blockers. See [the report layer](report-layer.md).

## Contracting for it: agile, time and materials, measured by a QASP

The toolkit fits a modular, agile acquisition: a time-and-materials order for a product team that delivers
working software every sprint, with quality measured through a Quality Assurance Surveillance Plan (QASP)
rather than through acceptance of documents. It does not need a deliverables-based contract or a separate
certification contract.

### In the Statement of Objectives

State outcomes, not tasks. Suggested objectives you can adapt:

> **Continuous certification readiness.** The contractor shall maintain evidence of the system's readiness
> for CMS Streamlined Modular Certification and FNA SNAP system approval throughout development, not only
> before reviews. Automated tests that prove a certification rule shall carry that rule's key from the
> pinned rules catalog; the contractor's pipeline shall run the continuous certification checks on every
> pull request and publish the evidence bundle and static report on every build of the main branch.

> **Testable eligibility decisions.** The system shall expose, in test environments, a determination
> interface that accepts household facts and returns the eligibility decision and benefit, so that the
> State's golden test cases can run automatically.

> **Measurable operations from the first sprint.** The contractor shall maintain queries for the federal
> operational metrics against the metric data contract from the first sprint, and shall run them against
> synthetic data as soon as the data model exists.

Also name, in the order:

- the **released toolkit version** and the **pinned catalog version**, with catalog updates adopted only
  through change control;
- that, **until the named toolkit release exists**, the contractor's only obligation is tagged, standard
  test reports (JUnit XML or Cucumber JSON);
- that work to fill toolkit gaps is **ordinary backlog work** under the order's ceiling, prioritized by the
  State's product owner;
- that **UAT and pilot testing are performed by the State**, and their results recorded by a State-owned
  pipeline or test-management tool, consistent with FNS Handbook 901 §6.7.2–6.7.3.

### In the Definition of Done

Add to the team's Definition of Done for any story that touches a certification rule:

- its tests carry the rule key, and `check-tags` reports no errors;
- the certification check shows no new regressions on the pull request;
- the change does not add an automated accessibility failure or an unresolved medium or high security finding.

### QASP additions

Add these measures to the State's existing QASP. General quality measures (test coverage, code style,
deployment) stay in that QASP, as in [18F's sample agile QASP](https://guides.18f.org/derisking/qasp/).
The State's contracting officer's representative or product owner reviews them at the end of every sprint,
from the static report. They cover only vendor-owned work and never count the State's own timeliness
against the contractor.

| Measure | Performance standard | Acceptable quality level | Assessed by |
| --- | --- | --- | --- |
| Certification traceability | Tests for work that touches a catalog rule carry its rule key | 0 `check-tags` errors; every story linked to a rule has at least one tagged test by sprint end | Pipeline `check-tags` and the static report |
| Evidence availability | Every build on main publishes its evidence bundle | 100% of main builds | Pipeline artifacts |
| Regression restoration | Vendor-owned regressions in tagged tests are restored quickly | 95% restored within 5 working days | Time to restore in the report layer |
| Test reliability | Flaky tagged tests are fixed, not ignored | Every quarantined test fixed or removed within 2 sprints | Quarantine list in the static report |
| Metric readiness | ORW and Go Live metric queries compile and run | 100% compile every sprint; 100% run against synthetic data once the data model exists | Nightly pipeline check |
| Golden case correctness | System results match the State's expected outcomes | 100% of undisputed cases for rules in the sprint's scope pass | Golden case suite |
| Certification defect data | Defects carry severity, dates, and linked rules | 100% of defects on tagged rules have severity and dates; 0 open critical defects in features demonstrated as done | Defect tracker export |
| Accessibility evidence | Automated WCAG 2.2 AA results published as CEF12 evidence | Results published every build; 0 automated errors in features demonstrated as done | Automated scanner in CI |
| Security evidence | Pipeline scan results published to feed the POA&M | Results published every build; 0 unresolved medium or high findings, false positives documented | Static analysis, dependency, and dynamic scans in CI |

When a measure falls short, the usual QASP path applies: discussion at the sprint review, then a corrective
action plan, then the remedies in the order. Whether CMS or FNA approves the system is not a contractor
measure, because neither agency's decision is in the contractor's control.

### Who owns what

| Artifact | Default owner |
| --- | --- |
| Rule tags on tests; the system adapter for golden cases and example tests | Contractor |
| Metric queries against the metric data contract | Contractor |
| `capd.yaml` and the State profile (State outcomes, N/A justifications, thresholds, gate order) | State, with contractor input |
| Golden case expected outcomes | State policy staff |
| Report layer: loads of external data, roles, dashboards | State data team |
| Acceptance of evidence; checklists, letters, and signatures | State |
| Independent assessments, IV&V ratings | Third parties named in the order |

### Working rhythm

| When | What happens |
| --- | --- |
| Every pull request | The certification check comments on regressions; in report-only mode it never blocks |
| Every sprint review | The product owner reviews the static report and the QASP measures; accepted evidence is recorded |
| Every day | The static report is published to the private reports repository from main |
| When the team agrees | The State and the contractor switch the gate from report-only to blocking, through a reviewed change |
| Before each gate | The dashboard lists the open blockers; nobody assembles evidence by hand |

## What your team provides

| You provide | Used for | Sample |
| --- | --- | --- |
| Gate dates and the agreed gate order, once CMS and FNA rule | The calendar and "At risk" warnings | [`gates.csv`](../report-layer/sample-data/gates.csv) |
| State outcomes and N/A justifications | The catalog for your project | [`capd.yaml`](../templates/config/capd.yaml) |
| Expected outcomes for golden test cases (policy staff) | Golden case correctness; the contractor can dispute a case | [`golden-cases/`](../examples/golden-cases/) |
| Tracked items: letters, plans, assessments, demonstrations | Rules that rest on documents and attestations | [`tracked_items.csv`](../report-layer/sample-data/tracked_items.csv) |
| Acceptance decisions (product owner) | Rules that need State acceptance before they count as Met | [`acceptances.csv`](../report-layer/sample-data/acceptances.csv) |
| A mapping from the metric contract to your tables | Production metrics for the CR and the Go Live numbers | [`mapping.yaml`](../templates/config/mapping.yaml) |

## What it does not do

- **It does not replace CMS or FNA judgment.** Met is a readiness signal, not "Evidence Satisfactory" or
  FNA's concurrence.
- **It does not write the APD, the contract, or the security assessment.** It tracks their dates and status.
- **It does not model cost allocation or other financial approvals.** Those appear only as tracked dates.
- **It does not read real case data into reports.** Static reports carry pipeline data only, and aggregates
  from case data suppress counts under 11.

Start with the [five-minute demo](../README.md#see-it-in-five-minutes), then read the [proposal](proposal.md)
for the federal rules behind each choice.

*Suggested contract language is a starting point for the State's procurement and legal staff, not legal advice.*
