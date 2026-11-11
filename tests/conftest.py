import importlib.util
import sys
from pathlib import Path

import pytest

from capd.catalog import Catalog
from capd.connectors.base import RunContext

ROOT = Path(__file__).resolve().parents[1]
FIX = Path(__file__).parent / "fixtures"


@pytest.fixture(scope="session")
def catalog():
    return Catalog.load()


@pytest.fixture
def ctx(catalog):
    return RunContext(build_id="b1", commit="a" * 40, branch="main", catalog=catalog, observed_at="2026-11-11T12:00:00Z")


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod
