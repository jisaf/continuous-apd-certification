import json

from capd.compare import MARKER, compare, markdown
from capd.connectors.azure_devops import AzureDevOpsSink
from capd.connectors.chat import ChatDigestSink
from capd.connectors.file_sink import FileSink, rows
from capd.connectors.github import GitHubSink
from capd.connectors.jira import JiraSink
from capd.connectors.junit import JUnitSource
from capd.connectors.snowflake import SnowflakeSink
from capd.connectors.testing import check_sink
from capd.evidence import build_bundle

from .conftest import FIX


class Resp:
    def __init__(self, data=None):
        self.data = data if data is not None else {}

    def json(self):
        return self.data

    def raise_for_status(self):
        return None


class FakeSession:
    def __init__(self, gets=None):
        self.headers, self.calls, self.gets, self.auth = {}, [], gets or {}, None

    def get(self, url, **kw):
        self.calls.append(("GET", url, kw))
        for k, v in self.gets.items():
            if k in url:
                return Resp(v)
        return Resp({})

    def post(self, url, **kw):
        self.calls.append(("POST", url, kw))
        return Resp({"id": 7, "key": "CERT-1"})

    def patch(self, url, **kw):
        self.calls.append(("PATCH", url, kw))
        return Resp({"id": 7})

    def put(self, url, **kw):
        self.calls.append(("PUT", url, kw))
        return Resp({})


def result(ctx):
    b = build_bundle(ctx, JUnitSource().collect(ctx, {"paths": [str(FIX / "junit.xml")]}))
    c = compare(b, None)
    return {"bundle": b, "comparison": c, "markdown": markdown(c)}


def test_github_sticky_comment(ctx, monkeypatch):
    monkeypatch.setenv("GITHUB_TOKEN", "t")
    ctx.pull_request = "12"
    r = result(ctx)
    s = FakeSession({"/comments": []})
    out = GitHubSink().publish(r, ctx, {"repository": "o/r", "_session": s})
    assert out["action"] == "created" and s.calls[-1][0] == "POST"
    s2 = FakeSession({"/comments": [{"id": 5, "body": MARKER + " old"}]})
    assert GitHubSink().publish(r, ctx, {"repository": "o/r", "_session": s2})["action"] == "updated"
    s3 = FakeSession({"/comments": [{"id": 5, "body": r["markdown"]}]})
    assert GitHubSink().publish(r, ctx, {"repository": "o/r", "_session": s3})["action"] == "unchanged"


def test_github_skips_non_pr_builds(ctx, monkeypatch):
    monkeypatch.delenv("GITHUB_REPOSITORY", raising=False)
    assert "skipped" in GitHubSink().publish(result(ctx), ctx, {})


def test_azure_devops_summary_and_thread(ctx, tmp_path, monkeypatch):
    monkeypatch.setenv("SYSTEM_PULLREQUEST_PULLREQUESTID", "9")
    monkeypatch.setenv("SYSTEM_ACCESSTOKEN", "t")
    s = FakeSession({"/threads": {"value": []}})
    out = AzureDevOpsSink().publish(result(ctx), ctx, {"summaryPath": str(tmp_path / "s.md"), "collectionUri": "https://dev.azure.com/org",
                                                       "project": "p", "repositoryId": "r", "_session": s})
    assert out["action"] == "created" and (tmp_path / "s.md").exists()
    assert s.calls[-1][1].endswith("/pullRequests/9/threads")


def test_jira_plan_gate_and_blocker_issues(ctx):
    r = result(ctx)
    r["comparison"]["regressions"] = [{"testId": "t1", "name": "t1", "ruleIds": ["fna:sirt:S0215"], "was": "pass", "now": "fail"}]
    r["comparison"]["fixed"] = [{"testId": "t2", "name": "t2", "ruleIds": [], "was": "fail", "now": "pass"}]
    plan = JiraSink().plan(r)
    assert sum(1 for a in plan if a["label"].startswith("capd-gate-")) == 2
    assert any(a["op"] == "upsert" and a["label"] == "capd-blocker-t1" for a in plan)
    assert any(a["op"] == "close" and a["label"] == "capd-blocker-t2" for a in plan)
    s = FakeSession({"/search": {"issues": []}})
    out = JiraSink().publish(r, ctx, {"baseUrl": "https://jira.example", "_session": s})
    assert len(out["results"]) == 3


def test_chat_posts_only_on_change(ctx, tmp_path, monkeypatch):
    monkeypatch.setenv("CAPD_CHAT_WEBHOOK", "https://hooks.example/x")
    r = result(ctx)
    opts = {"stateFile": str(tmp_path / "state.json"), "_session": FakeSession()}
    assert ChatDigestSink().publish(r, ctx, opts)["action"] == "posted"
    assert ChatDigestSink().publish(r, ctx, opts)["action"] == "unchanged"


def test_file_and_snowflake_rows(ctx, tmp_path):
    r = result(ctx)
    FileSink().publish(r, ctx, {"dir": str(tmp_path)})
    lines = (tmp_path / "evidence-rows.ndjson").read_text().splitlines()
    assert len(lines) == len(rows(r["bundle"])) and json.loads(lines[0])["build_id"] == "b1"
    stmts = SnowflakeSink().statements(r["bundle"], {})
    assert stmts[0][0].startswith("DELETE FROM CERTIFICATION.CERT.EVIDENCE") and len(stmts) == 3 + len(lines)


def test_builtin_sinks_pass_the_conformance_kit(tmp_path):
    for sink, opts in ((FileSink(), {"dir": str(tmp_path)}), (GitHubSink(), {}), (JiraSink(), {"baseUrl": "https://x"}),
                       (ChatDigestSink(), {"stateFile": str(tmp_path / "c.json")}), (SnowflakeSink(), {}),
                       (AzureDevOpsSink(), {"summaryPath": str(tmp_path / "s.md"), "prComment": False})):
        check_sink(sink, opts)
