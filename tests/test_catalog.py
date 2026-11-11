import json

from capd import schemas
from capd.catalog import Catalog, is_key

from .conftest import ROOT, load_module


def test_counts_and_keys(catalog):
    s = catalog.summary()["bySet"]
    assert s == {"cms:ee": 27, "cms:cef": 22, "fna:sirt": 821, "fna:golive": 26}
    assert all(is_key(k) for k in catalog.rules)


def test_every_rule_matches_schema(catalog):
    for r in catalog.rules.values():
        assert not schemas.errors("catalog-rule", r), r["key"]


def test_stable_keys_do_not_move(catalog):
    # Published keys never change meaning. These pin a few by their FNA/CMS source IDs.
    assert catalog.get("fna:sirt:S0001")["sourceId"] == "AP-1"
    assert catalog.get("fna:sirt:S0215")["sourceId"] == "OD-1"
    assert catalog.get("fna:sirt:S0109")["sourceId"] == "EI-13"
    assert catalog.get("fna:golive:GL03")["title"] == "Current program performance"


def test_programs_are_inferred(catalog):
    assert catalog.programs_for(["cms:ee:EE5"]) == ["medicaid"]
    assert catalog.programs_for(["fna:sirt:S0215"]) == ["snap"]
    assert catalog.programs_for(["cms:ee:EE21"]) == ["medicaid", "snap"]
    assert catalog.programs_for(["cms:ee:EE5", "fna:sirt:S0215"]) == ["medicaid", "snap"]


def test_overrides_and_state_rules():
    cat = Catalog.load(
        state_rules=[{"key": "state:ee:STEE01", "agency": "state", "set": "ee", "sourceId": "STEE01", "title": "Faster renewals",
                      "programs": ["medicaid"], "gates": {"CR": ["metric"]}, "responsibility": "shared",
                      "coverage": "evidenced", "acceptance": "not_required", "freshnessDays": 45, "source": {"document": "APD"}}],
        overrides={"cms:ee:EE12": {"applicable": False, "justification": "separate module"}})
    assert "state:ee:STEE01" in cat
    assert not cat.applicable("cms:ee:EE12")
    assert all(r["key"] != "cms:ee:EE12" for r in cat.rules_for_gate("ORR"))


def test_committed_catalog_matches_a_fresh_build():
    builder = load_module("build_catalog", ROOT / "tools" / "build_catalog.py")
    committed = json.loads((ROOT / "src/capd/data/catalog/catalog.json").read_text())
    assert builder.build() == committed, "run: python tools/build_catalog.py"
