"""The core connector interface. Every connector implements one of these two protocols.

A source connector reads pipeline-produced artifacts (test reports, scan results) and returns
evidence records. A sink connector publishes a run's results somewhere (a pull request comment,
a CI summary, Jira, a chat channel, a data platform). Connectors must not read external systems
of record into the evidence bundle: external data joins only in the report layer.
"""

from __future__ import annotations

import importlib
from dataclasses import dataclass, field
from importlib import metadata
from typing import Any, Protocol, runtime_checkable

from ..evidence import now_iso


@dataclass
class RunContext:
    build_id: str
    commit: str
    branch: str = ""
    pipeline: str = ""
    build_url: str = ""
    pull_request: str = ""
    environment: str = "ci"
    executed_by: str = "automation"
    observed_at: str = field(default_factory=now_iso)
    catalog: Any = None
    config: dict = field(default_factory=dict)
    dry_run: bool = False
    warnings: list[str] = field(default_factory=list)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)


@runtime_checkable
class SourceConnector(Protocol):
    id: str
    config_schema: dict

    def collect(self, ctx: RunContext, options: dict) -> list[dict]:
        """Return evidence records (see schemas/evidence-record.schema.json)."""


@runtime_checkable
class SinkConnector(Protocol):
    id: str
    config_schema: dict

    def publish(self, result: dict, ctx: RunContext, options: dict) -> dict:
        """Publish a run result. Return a dict describing what was (or, in dry-run, would be) sent."""


BUILTIN = {
    "junit": "capd.connectors.junit:JUnitSource",
    "cucumber": "capd.connectors.cucumber:CucumberSource",
    "sarif": "capd.connectors.sarif:SarifSource",
    "axe": "capd.connectors.axe:AxeSource",
    "file": "capd.connectors.file_sink:FileSink",
    "github": "capd.connectors.github:GitHubSink",
    "azure-devops": "capd.connectors.azure_devops:AzureDevOpsSink",
    "jira": "capd.connectors.jira:JiraSink",
    "chat": "capd.connectors.chat:ChatDigestSink",
    "snowflake": "capd.connectors.snowflake:SnowflakeSink",
}


def _load_ref(ref: str):
    mod, _, attr = ref.partition(":")
    return getattr(importlib.import_module(mod), attr)


def available() -> dict[str, str]:
    """All registered connectors: built-ins plus any installed package exposing 'capd.connectors' entry points."""
    found = dict(BUILTIN)
    try:
        for ep in metadata.entry_points(group="capd.connectors"):
            found[ep.name] = ep.value
    except Exception:  # pragma: no cover - metadata edge cases
        pass
    return found


def get(name: str):
    refs = available()
    if name not in refs:
        raise KeyError(f"unknown connector '{name}'. Installed: {', '.join(sorted(refs))}")
    return _load_ref(refs[name])()
