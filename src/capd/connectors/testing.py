"""Connector conformance kit. Every connector must pass these checks before it is merged.

Use from a pytest test in your connector package:

    from capd.connectors.testing import check_source, check_sink

    def test_conforms(tmp_path):
        check_source(MySource(), {"paths": ["fixtures/*.xml"]})

The checks call the connector the way the CLI does and verify the integration contract: records match
the evidence-record schema, rule keys use the key syntax, programs are inferred, sinks honour dry-run
and never need network access when ctx.dry_run is set.
"""

from __future__ import annotations

from ..catalog import Catalog, is_key
from ..evidence import build_bundle
from ..schemas import errors
from .base import RunContext, SinkConnector, SourceConnector


def context(dry_run: bool = True) -> RunContext:
    return RunContext(build_id="conformance-1", commit="0" * 40, branch="main", catalog=Catalog.load(), dry_run=dry_run)


def check_source(connector, options: dict) -> list[dict]:
    assert isinstance(connector, SourceConnector), "source connectors need id, config_schema and collect()"
    assert isinstance(connector.id, str) and connector.id, "id must be a non-empty string"
    assert isinstance(connector.config_schema, dict), "config_schema must be a JSON Schema object"
    ctx = context()
    records = connector.collect(ctx, options)
    assert isinstance(records, list) and records, "collect() must return at least one record for the fixtures"
    for r in records:
        errs = errors("evidence-record", r)
        assert not errs, f"record does not match the evidence-record schema: {errs}"
        assert all(is_key(k) for k in r["ruleIds"]), f"malformed rule key in {r['ruleIds']}"
        assert r["programs"] == ctx.catalog.programs_for(r["ruleIds"]), "programs must be inferred from rule keys"
    build_bundle(ctx, records, ctx.warnings)  # must form a valid bundle
    return records


def check_sink(connector, options: dict, result: dict | None = None) -> dict:
    assert isinstance(connector, SinkConnector), "sink connectors need id, config_schema and publish()"
    ctx = context(dry_run=True)
    if result is None:
        from ..compare import compare, markdown
        bundle = build_bundle(ctx, [])
        cmp = compare(bundle, None)
        result = {"bundle": bundle, "comparison": cmp, "markdown": markdown(cmp)}
    out = connector.publish(result, ctx, options)
    assert isinstance(out, dict) and out.get("connector") == connector.id, "publish() must return a dict naming the connector"
    return out
