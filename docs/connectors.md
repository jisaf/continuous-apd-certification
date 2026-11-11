# Writing a connector

A connector links capd to one outside tool. Every connector implements one small interface, passes a
shared conformance kit, and ships as its own Python package. Adding one never needs a change to the core.

## The two kinds

| Kind | Interface | Job | Built in |
| --- | --- | --- | --- |
| **Source** | `collect(ctx, options) -> list[evidence record]` | Read a report the pipeline produced and return evidence records | `junit`, `cucumber`, `playwright`, `sarif`, `axe` |
| **Sink** | `publish(result, ctx, options) -> dict` | Send a run's results somewhere | `file`, `github`, `azure-devops`, `jira`, `chat`, `snowflake` |

Both are defined in [`src/capd/connectors/base.py`](../src/capd/connectors/base.py):

```python
class SourceConnector(Protocol):
    id: str                 # the name used in capd.yaml, for example "trx"
    config_schema: dict     # JSON Schema for the connector's options
    def collect(self, ctx: RunContext, options: dict) -> list[dict]: ...

class SinkConnector(Protocol):
    id: str
    config_schema: dict
    def publish(self, result: dict, ctx: RunContext, options: dict) -> dict: ...
```

Rules every connector follows:

1. **Sources read pipeline-produced data only.** Never pull Jira, production data, or security findings
   into the evidence bundle; those belong in the report layer.
2. **Records match the schema.** [`evidence-record.schema.json`](../src/capd/data/schemas/evidence-record.schema.json)
   is the contract. Build records with `capd.evidence.make_record` (or `capd.connectors._common.test_records`
   for test results), which fills build details and infers programs from rule keys.
3. **Sinks honour dry-run.** When `ctx.dry_run` is true, return what would be sent and make no network call.
4. **Secrets come from environment variables** (pipeline secret variables), never from `capd.yaml`.
5. **Sinks speak only on change.** Update one comment or issue in place, and post only when the content changed.

## Step by step: the TRX example

[`examples/connector-template/`](../examples/connector-template/) is a complete connector for Visual Studio
TRX test results. Copy it and rename it.

1. **Package.** `pyproject.toml` declares the entry point capd uses to find the connector:

   ```toml
   [project.entry-points."capd.connectors"]
   trx = "capd_trx:TrxSource"
   ```

2. **Code.** [`src/capd_trx/__init__.py`](../examples/connector-template/src/capd_trx/__init__.py) parses the
   file into simple cases (`testId`, `name`, `result`, `keys`, `sourceUri`) and hands them to
   `test_records`, which merges reruns, checks keys against the catalog, and infers programs. Rule keys come
   from `[TestCategory("rule:cms:ee:EE21")]`; `capd.tags.parse_tag` reads that form.

3. **Fixture and tests.** Put a small, synthetic sample report in `tests/fixtures/`, then run the shared kit:

   ```python
   from capd.connectors.testing import check_source

   def test_conforms():
       check_source(TrxSource(), {"paths": ["tests/fixtures/sample.trx"]})
   ```

   `check_source` checks the protocol, schema-valid records, valid rule keys, inferred programs, and that the
   records form a valid bundle. For sinks, `check_sink` calls `publish` in dry-run mode and checks the reply.

4. **Install and use.**

   ```sh
   pip install -e .
   capd connectors            # lists trx
   ```

   ```yaml
   sources:
     - connector: trx
       paths: ["TestResults/*.trx"]
   ```

For a sink, follow the built-in [`github.py`](../src/capd/connectors/github.py) (sticky pull request comment)
or [`jira.py`](../src/capd/connectors/jira.py) (one issue per gate). Accept an injected HTTP session through
`options["_session"]` so tests can use a fake, as [`tests/test_sinks.py`](../tests/test_sinks.py) does.

## Contributing a connector back

1. Fork this repository and create a branch.
2. Add the connector under `src/capd/connectors/` (built in) or as a package under `examples/` (plugin), with
   tests that use the conformance kit and only synthetic fixtures.
3. Run `ruff check` and `pytest`.
4. Commit with a sign-off (`git commit -s`): see [`CONTRIBUTING.md`](../CONTRIBUTING.md).
5. Open a pull request that describes the tool, the report format, and how you tested it.
