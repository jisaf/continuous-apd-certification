"""Small HTTP helper so sinks can be tested with a fake session and run in dry-run mode."""

from __future__ import annotations

import os


def session(options: dict):
    if options.get("_session") is not None:
        return options["_session"]
    import requests
    return requests.Session()


def secret(options: dict, key: str, env: str) -> str | None:
    """Secrets come from the environment (pipeline secret variables), never from config files."""
    name = options.get(key, env)
    return os.environ.get(name)
