# Connector template: a TRX source connector

A complete, working example of adding a connector to capd as a separate package. It reads Visual
Studio TRX test results (common for .NET teams on Azure DevOps) and turns `[TestCategory("rule:...")]`
attributes into evidence records. Copy this folder to start your own connector.

```sh
pip install -e ../..            # capd itself, from the repository root
pip install -e .                # this connector
pytest                          # runs the shared conformance kit and the connector's own tests
capd connectors                 # "trx" now appears in the list
```

Then use it in `capd.yaml`:

```yaml
sources:
  - connector: trx
    paths: ["TestResults/*.trx"]
```

The step-by-step guide is [`docs/connectors.md`](../../docs/connectors.md).
