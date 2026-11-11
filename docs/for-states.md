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

## How you see it

1. **Static report per build** (no hosting). The vendor's pipeline publishes it to a private reports
   repository once a day. It shows only pipeline data. See the [sample](sample-report/pull-request-build.html)
   and [how to read it](reading-the-report.md).
2. **Pull request comments, Jira gate issues, chat digests** in the tools your team already uses.
3. **The report layer and dashboard** (optional) on your existing data platform, for example Snowflake. Here
   pipeline evidence joins your tracked items, acceptance decisions, production metrics, and gate dates to
   give each rule a status and list blockers. See [the report layer](report-layer.md).

## What to put in the solicitation

The proposal has the details; in short:

- **Use the toolkit** at a named, released version, with the catalog version pinned and updates through
  change control. Until that release exists, require only tagged, standard test reports.
- **Tag tests with rule keys,** feed the pipeline step, and publish the evidence bundle on every main build.
- **Expose a test-facing determination API** in test environments, so golden test cases run through a small
  adapter rather than through the user interface.
- **Write metric queries against the metric data contract** from the first sprint, and run them on
  synthetic data once the data model exists.
- **Add the certification measures to your QASP:** traceability, evidence availability, regression
  restoration, test reliability, metric readiness, golden case correctness, defect data, and accessibility
  and security evidence. See "Recommended QASP additions" in the [proposal](proposal.md).
- **Name an owner for each artifact.** The proposal's ownership table is a starting point.

## What your team provides

| You provide | Used for |
| --- | --- |
| Gate dates and the agreed gate order, once CMS and FNA rule | The calendar and "At risk" warnings |
| State-specific outcomes and N/A justifications (`capd.yaml`) | The catalog for your project |
| Expected outcomes for golden test cases (policy staff) | Golden case correctness; the vendor can dispute a case |
| Tracked items: letters, plans, assessments, demonstrations | Rules that rest on documents and attestations |
| Acceptance decisions (product owner) | Rules that need state acceptance before they count as Met |
| A `mapping.yaml` from the metric contract to your tables | Production metrics for the CR and the Go Live numbers |

## What it does not do

- **It does not replace CMS or FNA judgment.** Met is a readiness signal, not "Evidence Satisfactory" or
  FNA's concurrence.
- **It does not write the APD, the contract, or the security assessment.** It tracks their dates and status.
- **It does not model cost allocation or other financial approvals.** Those appear only as tracked dates.
- **It does not read real case data into reports.** Static reports carry pipeline data only, and aggregates
  from case data suppress counts under 11.

Start with the [five-minute demo](../README.md#see-it-in-five-minutes), then read the [proposal](proposal.md)
for the federal rules behind each choice.
