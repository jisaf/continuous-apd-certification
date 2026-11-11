# Contributing

Thank you for helping. States, vendors, IV&V teams, federal reviewers, and developers are all welcome.

## Ways to help

- **Corrections** to how we read CMS and FNA requirements, with a citation to the source.
- **Connectors** for other tools: see [`docs/connectors.md`](docs/connectors.md).
- **Golden test cases** from public, licensed sources: see [`examples/golden-cases/`](examples/golden-cases/).
- **Report-layer adaptations** for other data platforms (BigQuery, Databricks, SQL Server, Postgres).
- **Experience**: what slowed your last ORR, CR, UAT Go/No-Go, or pilot.

Open an issue first for anything large.

## Ground rules

- **Never include real case data.** No applicant or recipient names, identifiers, case numbers, screenshots
  of real cases, or protected health information, in issues, pull requests, tests, fixtures, or examples.
- **Never include security findings** about any real system.
- **Cite sources** for any rule: document, section, and a link.
- **Respect licenses.** Do not copy material whose license is incompatible (see "Third-party material" in
  [`LICENSING.md`](LICENSING.md)).

## Development setup

```sh
python -m venv .venv && . .venv/bin/activate
pip install -e ".[dev]"
pytest                                       # unit, integration, and report-layer (DuckDB) tests
ruff check src tests tools report-layer
examples/sample-system/run-demo.sh           # end-to-end demo
```

Generated files must stay in sync with their sources; CI checks this:

```sh
python tools/build_catalog.py    # rules catalog, from catalog/sources and docs/research/classification
python tools/build_packs.py      # pre-written Gherkin packs, from the catalog
```

Rule keys are permanent. Never renumber or reuse a key; add new rules with new keys and record changes in
the catalog's change log.

## Pull requests

1. Fork and branch from `main`.
2. Add tests. Connectors must pass the conformance kit (`capd.connectors.testing`).
3. Run `pytest` and `ruff check`.
4. Sign off each commit under the [Developer Certificate of Origin](https://developercertificate.org/):

   ```sh
   git commit -s -m "Describe the change"
   ```

   The sign-off certifies that you wrote the change or otherwise have the right to submit it under the
   project's licenses (Apache-2.0 for code, CC0 for data and documentation). There is no contributor
   license agreement. A CI check (`.github/workflows/dco.yml`) fails a pull request with any unsigned
   commit; fix it with `git rebase --signoff origin/main` and push again.
5. Open the pull request with a short description of the change and how you tested it.
