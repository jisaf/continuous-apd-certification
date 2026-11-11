"""Load capd.yaml (state and project configuration)."""

from __future__ import annotations

from pathlib import Path

import yaml

from . import schemas

DEFAULTS = {
    "environment": "ci",
    "gateMode": "report-only",
    "taggedPaths": [],
    "sources": [],
    "sinks": [],
    "stateRules": [],
    "ruleOverrides": {},
}


def load(path: str | Path | None) -> dict:
    data: dict = {}
    if path:
        p = Path(path)
        data = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
        data["_dir"] = str(p.resolve().parent)
    else:
        data = {"catalogVersion": "1.0.0", "_dir": str(Path.cwd())}
    clean = {k: v for k, v in data.items() if not k.startswith("_")}
    schemas.check("config", clean)
    out = dict(DEFAULTS)
    out.update(data)
    return out


def resolve(cfg: dict, rel: str) -> Path:
    p = Path(rel)
    return p if p.is_absolute() else Path(cfg.get("_dir", ".")) / p
