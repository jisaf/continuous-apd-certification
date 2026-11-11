"""Load and apply the packaged JSON Schemas (the integration contract)."""

from __future__ import annotations

import json
from functools import cache
from importlib import resources

from jsonschema import Draft202012Validator
from referencing import Registry, Resource

NAMES = ["evidence-record", "evidence-bundle", "catalog-rule", "test-case", "config"]


@cache
def schema(name: str) -> dict:
    text = resources.files("capd.data.schemas").joinpath(f"{name}.schema.json").read_text(encoding="utf-8")
    return json.loads(text)


@cache
def _registry() -> Registry:
    reg = Registry()
    for n in NAMES:
        s = schema(n)
        res = Resource.from_contents(s)
        reg = reg.with_resource(s["$id"], res).with_resource(f"{n}.schema.json", res)
    return reg


def validator(name: str) -> Draft202012Validator:
    return Draft202012Validator(schema(name), registry=_registry())


def errors(name: str, obj) -> list[str]:
    """Return human-readable validation errors (empty list when valid)."""
    out = []
    for e in sorted(validator(name).iter_errors(obj), key=lambda e: list(e.path)):
        where = "/".join(str(p) for p in e.path) or "(root)"
        out.append(f"{where}: {e.message}")
    return out


def check(name: str, obj) -> None:
    errs = errors(name, obj)
    if errs:
        raise ValueError(f"{name} is not valid:\n  " + "\n  ".join(errs[:20]))
