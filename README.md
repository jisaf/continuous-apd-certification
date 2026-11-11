# Continuous APD Certification

Open tools that let a state see, at any time, how close a Medicaid and SNAP eligibility system is to federal certification — instead of finding out at the end of the project.

> **Status: planning.** This repository holds the goals, the design proposal, the research behind it, and the decisions made so far. No code has been written yet.

## The problem

States that build Medicaid and SNAP systems with federal funds must pass two federal reviews:

- **CMS Streamlined Modular Certification (SMC):** an Operational Readiness Review (ORR) before go-live and a Certification Review (CR) after at least six months in production, followed by monthly operational reporting.
- **USDA Food and Nutrition Administration (FNA) testing gates under 7 CFR 277.18:** a Complete and Final Test Plan before UAT, a Go/No-Go decision after UAT, and a second Go/No-Go after a live pilot of usually at least three months.

Most of the evidence these reviews need is produced every day by the vendor's delivery work — tests, defects, builds, and production data — but it is gathered by hand into spreadsheets and uploaded weeks before each review. The state's Medicaid director usually sees the full picture late, when problems are most expensive to fix.

## The goal

Make certification readiness **continuous and visible**:

- A vendor's pipeline checks certification rules on every build, the same way it runs tests.
- A state Medicaid director can see, every sprint, which outcomes are tested, measured, and evidenced, and what blocks the next review.
- Review packages (SMC Intake Form, Operational Report Workbook, SNAP SIRT response, Go/No-Go evidence) are generated from evidence, in the agencies' own templates, not assembled by hand.
- One evidence set serves both CMS and FNA for an integrated eligibility system.

The model is CMS's own [Hospital Price Transparency tools](https://cmsgov.github.io/hpt-tool/): a published, versioned rule set, one validator behind a browser page and a CLI, and plain guidance.

## Design principles

1. **Generic and plug-and-play**, built for the engineers who wire it into a pipeline.
2. **Independent but additive modules.** The pipeline tools work alone. Evidence history and dashboards add value on top, and never the other way round.
3. **Pre-written examples where the test is known** — for example, 588 of the 821 SNAP SIRT rows are single, checkable behaviours.
4. **Connectors against one core interface.** GitHub, Azure DevOps, Jira, Snowflake, email, and chat are plugins; adding one is a documented, tested process.
5. **Mapping is configuration; extension is code.** No state will reshape its data for this toolkit, so the toolkit maps to each state's data.
6. **No new hosting.** Static HTML reports per build first, built from pipeline data only. External data (production metrics, security findings, Jira defects) joins only in an optional report layer on the state's existing data platform and BI tools, delivered mostly as patterns and templates. A hosted application is deliberately out of scope for now, because it would trigger a separate security review in every state.

![Static reports use pipeline data only; external data joins in the optional report layer](docs/images/architecture.png)

## First project

The first project is one state, not named publicly. The assumed profile: a full rebuild of an integrated Medicaid and SNAP eligibility system by an agile-first vendor, using GitHub for code, Azure DevOps for pipelines, Jira for issues, and Snowflake for metrics. The toolkit itself stays state-neutral: everything state-specific is configuration.

## What is here

| Path | Contents |
| --- | --- |
| [`docs/proposal.md`](docs/proposal.md) | The full proposal: the rules, prior art, design, vendor workflow, director views, risk and time savings, roadmap, decisions, and open questions |
| [`docs/next-steps.md`](docs/next-steps.md) | What happens next, in order |
| [`docs/research/`](docs/research/) | Row-by-row classification of the CMS E&E outcomes, CEFs, SNAP SIRT, and Go Live criteria, and notes on FNS Handbook 901 and CMS SHO #25-003 |
| [`LICENSING.md`](LICENSING.md) | How code, data, and documents are licensed |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | How to contribute, with a Developer Certificate of Origin sign-off |
| [`NOTICE.md`](NOTICE.md) | Sources and attributions |

## Licensing in short

Fully open source, with no commercial license:

- **Code**, including connectors: [Apache License 2.0](LICENSE).
- **Rules data, examples, and documentation:** [CC0 1.0](LICENSE-DATA) (public domain dedication).

See [`LICENSING.md`](LICENSING.md) for details and how third-party licenses are respected.

## Disclaimer

This is an independent project. It is not affiliated with, endorsed by, or an official product of CMS, USDA, FNA, or any state. Federal guidance is quoted for convenience; the agencies' own published documents are authoritative. Nothing here is legal advice.
