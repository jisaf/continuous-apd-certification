
import yaml

from capd import schemas
from capd.config import load

from .conftest import ROOT


def test_golden_cases_match_the_schema():
    files = sorted((ROOT / "examples" / "golden-cases").rglob("*.yaml"))
    assert files
    n = 0
    for f in files:
        for case in yaml.safe_load(f.read_text()):
            assert not schemas.errors("test-case", case), (f, case["id"])
            n += 1
    assert n >= 37


def test_config_templates_validate():
    for p in [ROOT / "examples/sample-system/capd.yaml", ROOT / "examples/sample-system/capd-ci.yaml", ROOT / "templates/config/capd.yaml"]:
        assert load(p)["catalogVersion"] == "1.0.0", p


def test_sirt_packs_use_real_keys(catalog):
    packs = sorted((ROOT / "examples" / "packs").rglob("*.feature"))
    assert packs
    for f in packs:
        for tag in [t for t in f.read_text().split() if t.startswith("@rule:")]:
            assert tag[len("@rule:"):] in catalog, (f, tag)


def test_docs_reference_existing_files():
    for doc in (ROOT / "docs").glob("*.md"):
        for link in __import__("re").findall(r"\]\(((?!https?:|#|mailto:)[^)#\s]+)", doc.read_text()):
            assert (doc.parent / link).exists() or (ROOT / link).exists(), f"{doc.name}: broken link {link}"
    readme = (ROOT / "README.md").read_text()
    for link in __import__("re").findall(r"\]\(((?!https?:|#|mailto:)[^)#\s]+)", readme):
        assert (ROOT / link).exists(), f"README: broken link {link}"


def test_reference_workflow_matches_the_template():
    assert (ROOT / ".github/workflows/capd.yml").read_text() == (ROOT / "templates/github-actions/capd.yml").read_text()
