"""Static checks on templates that cannot run here: Snowflake SQL (parsed with a Snowflake-dialect parser)
and the Azure DevOps / GitHub Actions pipeline templates (structure and references)."""

import re

import pytest
import yaml

from .conftest import ROOT

sqlglot = pytest.importorskip("sqlglot")
LAYER = ROOT / "report-layer"


def statements(path):
    text = "\n".join(ln for ln in path.read_text().splitlines() if not ln.strip().startswith("--"))
    return [s.strip() for s in text.split(";") if s.strip()]


@pytest.mark.parametrize("path", sorted((LAYER / "sql").rglob("*.sql")) + sorted((LAYER / "snowflake").glob("*.sql")),
                         ids=lambda p: str(p.relative_to(LAYER)))
def test_report_layer_sql_parses_as_snowflake(path):
    for stmt in statements(path):
        sqlglot.parse_one(stmt, read="snowflake")   # raises ParseError on invalid Snowflake SQL


def test_azure_step_template():
    t = yaml.safe_load((ROOT / "templates/azure-devops/capd-steps.yml").read_text())
    names = {p["name"] for p in t["parameters"]}
    assert {"config", "capdVersion", "pythonVersion", "mainBranch"} <= names
    tasks = [s.get("task") for s in t["steps"] if "task" in s]
    assert "DownloadPipelineArtifact@2" in tasks and "PublishPipelineArtifact@1" in tasks
    script = " ".join(s.get("script", "") for s in t["steps"])
    assert "capd run" in script and "--baseline" in script
    used = set(re.findall(r"parameters\.(\w+)", (ROOT / "templates/azure-devops/capd-steps.yml").read_text()))
    assert used <= names, f"undeclared parameters: {used - names}"
    publish = [s for s in t["steps"] if s.get("task") == "PublishPipelineArtifact@1"][0]
    download = [s for s in t["steps"] if s.get("task") == "DownloadPipelineArtifact@2"][0]
    assert publish["inputs"]["artifact"] == download["inputs"]["artifactName"] == "capd-evidence"


def test_azure_example_references_existing_templates():
    ex = yaml.safe_load((ROOT / "templates/azure-devops/azure-pipelines.example.yml").read_text())
    for step in ex["steps"]:
        if "template" in step:
            assert (ROOT / step["template"]).exists(), step["template"]
    pub = yaml.safe_load((ROOT / "templates/azure-devops/capd-publish-reports.yml").read_text())
    assert {p["name"] for p in pub["parameters"]} >= {"reportsRepo"}


def test_github_reusable_workflow():
    wf = yaml.safe_load((ROOT / "templates/github-actions/capd.yml").read_text())
    on = wf.get("on") or wf.get(True)          # YAML 1.1 reads "on" as True
    assert "workflow_call" in on
    steps = wf["jobs"]["capd"]["steps"]
    assert any("capd run" in s.get("run", "") for s in steps)
    assert any(s.get("with", {}).get("name") == "capd-evidence" for s in steps)
