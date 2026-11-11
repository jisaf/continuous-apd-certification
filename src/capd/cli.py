"""capd command-line interface.

    capd run --config capd.yaml                  collect, check tags, compare with main, write the report, publish
    capd collect --config capd.yaml -o out/bundle.json
    capd check-tags --bundle out/bundle.json --config capd.yaml
    capd compare --bundle out/bundle.json --baseline baseline/bundle.json
    capd report --bundle out/bundle.json --comparison out/comparison.json -o out/report.html
    capd publish --config capd.yaml --bundle out/bundle.json --comparison out/comparison.json
    capd validate orw|intake|sirt|templates|cases ...
    capd package check FNA-UAT submissions/fna-uat --bundle out/bundle.json -o out/package
    capd package verify out/package/submission-record.json --dir submissions/fna-uat
    capd catalog [--key KEY] [--search TEXT]
    capd connectors
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

import yaml

from . import __version__, schemas
from .catalog import Catalog
from .checktags import check as check_tags
from .compare import compare, load_quarantine, markdown
from .config import load as load_config
from .config import resolve
from .connectors import base as connectors
from .evidence import build_bundle
from .evidence import load as load_bundle
from .evidence import save as save_bundle
from .report.html import render

PATH_OPTIONS = ("dir", "stateFile", "summaryPath")


def build_info(args) -> dict:
    """Build metadata from flags, else from Azure Pipelines or GitHub Actions variables."""
    e = os.environ
    pr = getattr(args, "pull_request", None) or e.get("SYSTEM_PULLREQUEST_PULLREQUESTID") or ""
    ref = e.get("GITHUB_REF", "")
    if not pr and ref.startswith("refs/pull/"):
        pr = ref.split("/")[2]
    url = ""
    if e.get("SYSTEM_COLLECTIONURI") and e.get("BUILD_BUILDID"):
        url = f"{e['SYSTEM_COLLECTIONURI'].rstrip('/')}/{e.get('SYSTEM_TEAMPROJECT', '')}/_build/results?buildId={e['BUILD_BUILDID']}"
    elif e.get("GITHUB_RUN_ID"):
        url = f"{e.get('GITHUB_SERVER_URL', 'https://github.com')}/{e.get('GITHUB_REPOSITORY', '')}/actions/runs/{e['GITHUB_RUN_ID']}"
    return {
        "build_id": getattr(args, "build_id", None) or e.get("BUILD_BUILDID") or e.get("GITHUB_RUN_ID") or "local",
        "commit": getattr(args, "commit", None) or e.get("BUILD_SOURCEVERSION") or e.get("GITHUB_SHA") or "0" * 40,
        "branch": getattr(args, "branch", None) or e.get("BUILD_SOURCEBRANCHNAME") or e.get("GITHUB_HEAD_REF") or e.get("GITHUB_REF_NAME") or "",
        "pipeline": e.get("BUILD_DEFINITIONNAME") or e.get("GITHUB_WORKFLOW") or "",
        "build_url": url,
        "pull_request": pr,
    }


def make_ctx(args, cfg: dict, catalog: Catalog) -> connectors.RunContext:
    info = build_info(args)
    return connectors.RunContext(environment=getattr(args, "environment", None) or cfg.get("environment", "ci"),
                                 catalog=catalog, config=cfg, dry_run=getattr(args, "dry_run", False), **info)


def load_catalog(cfg: dict) -> Catalog:
    cat = Catalog.load(cfg.get("stateRules"), cfg.get("ruleOverrides"))
    pinned = cfg.get("catalogVersion")
    if pinned and pinned != cat.version:
        raise SystemExit(f"capd: configuration pins catalog {pinned}, but this capd ships catalog {cat.version}. "
                         "Catalog updates go through change control: update catalogVersion deliberately.")
    return cat


def cmd_collect(args, cfg=None, catalog=None) -> dict:
    cfg = cfg or load_config(args.config)
    catalog = catalog or load_catalog(cfg)
    ctx = make_ctx(args, cfg, catalog)
    sources = list(cfg.get("sources", []))
    for flag, name in (("junit", "junit"), ("cucumber", "cucumber"), ("sarif", "sarif"), ("axe", "axe")):
        if getattr(args, flag, None):
            sources.append({"connector": name, "paths": getattr(args, flag)})
    records = []
    for s in sources:
        opts = dict(s.get("options", {}))
        opts.setdefault("paths", s.get("paths", []))
        opts.setdefault("base", cfg.get("_dir"))
        if cfg.get("sidecarTags") and "sidecar" not in opts:
            opts["sidecar"] = str(resolve(cfg, cfg["sidecarTags"]))
        records.extend(connectors.get(s["connector"]).collect(ctx, opts))
    bundle = build_bundle(ctx, records, ctx.warnings)
    save_bundle(bundle, args.out)
    tagged = sum(1 for r in records if r["ruleIds"])
    print(f"capd: collected {len(records)} records ({tagged} tagged) into {args.out}")
    return bundle


def cmd_check_tags(args, cfg=None, catalog=None, bundle=None) -> int:
    cfg = cfg or load_config(args.config)
    catalog = catalog or load_catalog(cfg)
    bundle = bundle or load_bundle(args.bundle)
    issues = check_tags(bundle, catalog, cfg.get("taggedPaths"))
    for i in issues:
        print(f"check-tags: {i}")
    print(f"capd: check-tags found {len(issues)} issue(s)")
    return 1 if issues else 0


def _baseline(path) -> dict | None:
    if path and Path(path).exists():
        return load_bundle(path)
    if path:
        print(f"capd: no baseline at {path}; comparing against nothing (first run on this branch?)")
    return None


def cmd_compare(args, cfg=None, bundle=None) -> int:
    cfg = cfg or load_config(getattr(args, "config", None))
    bundle = bundle or load_bundle(args.bundle)
    qfile = args.quarantine or (str(resolve(cfg, cfg["quarantineFile"])) if cfg.get("quarantineFile") else None)
    mode = args.mode or cfg.get("gateMode", "report-only")
    result = compare(bundle, _baseline(args.baseline), load_quarantine(qfile), mode)
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(result, indent=1) + "\n", encoding="utf-8")
    md = markdown(result, getattr(args, "report_url", None))
    Path(args.markdown).write_text(md + "\n", encoding="utf-8")
    print(md)
    return 1 if result["blocking"] else 0


def cmd_report(args, catalog=None, bundle=None, comparison=None) -> None:
    bundle = bundle or load_bundle(args.bundle)
    if comparison is None and args.comparison and Path(args.comparison).exists():
        comparison = json.loads(Path(args.comparison).read_text())
    catalog = catalog or Catalog.load()
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(render(bundle, catalog, comparison, title=args.title), encoding="utf-8")
    print(f"capd: wrote static report {args.out}")


def cmd_publish(args, cfg=None, catalog=None, bundle=None, comparison=None) -> None:
    cfg = cfg or load_config(args.config)
    catalog = catalog or load_catalog(cfg)
    bundle = bundle or load_bundle(args.bundle)
    if comparison is None:
        comparison = json.loads(Path(args.comparison).read_text()) if args.comparison and Path(args.comparison).exists() else compare(bundle, None)
    ctx = make_ctx(args, cfg, catalog)
    result = {"bundle": bundle, "comparison": comparison, "markdown": markdown(comparison, args.report_url),
              "reportUrl": args.report_url}
    for sink in cfg.get("sinks", []):
        if args.only and sink["connector"] not in args.only:
            continue
        opts = dict(sink.get("options", {}))
        for k in PATH_OPTIONS:
            if isinstance(opts.get(k), str):
                opts[k] = str(resolve(cfg, opts[k]))
        out = connectors.get(sink["connector"]).publish(result, ctx, opts)
        print(f"capd: {json.dumps(out)[:400]}")


def cmd_run(args) -> int:
    cfg = load_config(args.config)
    catalog = load_catalog(cfg)
    out = Path(args.out_dir)
    args.out = str(out / "bundle.json")
    bundle = cmd_collect(args, cfg, catalog)
    tag_status = cmd_check_tags(args, cfg, catalog, bundle)
    args.bundle, args.out = args.out, str(out / "comparison.json")
    args.markdown = str(out / "summary.md")
    args.quarantine = None
    args.mode = None
    gate = cmd_compare(args, cfg, bundle)
    comparison = json.loads((out / "comparison.json").read_text())
    args.out, args.title, args.comparison = str(out / "report.html"), "Certification readiness report", None
    cmd_report(args, catalog, bundle, comparison)
    if not args.no_publish:
        args.only = None
        cmd_publish(args, cfg, catalog, bundle, comparison)
    strict = cfg.get("gateMode") == "blocking"
    return 1 if gate or (strict and tag_status) else 0


def cmd_validate(args, cfg=None) -> int:
    from .validators import intake, orw, templates

    if args.what == "templates":
        diffs = templates.orw_rules_conformance()
        for d in diffs:
            print(f"conformance: {d}")
        print(f"capd: pinned ORW template and ORW_Validation.xlsx disagree on {len(diffs)} point(s)" if diffs
              else "capd: pinned templates and rules agree")
        return 1 if diffs else 0
    if args.what == "cases":
        bad = 0
        files = sorted(Path(args.path).rglob("*.yaml")) if Path(args.path).is_dir() else [Path(args.path)]
        for f in files:
            for case in yaml.safe_load(f.read_text()) or []:
                errs = schemas.errors("test-case", case)
                if errs:
                    bad += 1
                    print(f"{f}: {case.get('id')}: {errs}")
        print(f"capd: checked test cases in {len(files)} file(s); {bad} invalid")
        return 1 if bad else 0
    cfg = cfg or load_config(getattr(args, "config", None))
    if args.what == "sirt":
        from .validators import sirt

        result = sirt.validate(args.path, load_catalog(cfg), load_bundle(args.bundle) if args.bundle else None)
    elif args.what == "orw":
        result = orw.validate(args.path)
    else:
        result = intake.validate(args.path, load_catalog(cfg), args.module)
    print(json.dumps(result, indent=1))
    return 1 if result["errors"] else 0


def cmd_package(args) -> int:
    from . import package

    if args.action == "verify":
        record = json.loads(Path(args.target).read_text(encoding="utf-8"))
        problems = package.verify(record, args.dir)
        for p in problems:
            print(f"capd: {p}")
        print("capd: submission record verified" if not problems else f"capd: {len(problems)} problem(s)")
        return 1 if problems else 0
    if not args.dir:
        raise ValueError("package check needs the package folder: capd package check GATE FOLDER")
    cfg = load_config(args.config)
    record = package.build(args.dir, args.target, load_catalog(cfg), args.bundle)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "submission-record.json").write_text(json.dumps(record, indent=1) + "\n", encoding="utf-8")
    (out / "checklist.md").write_text(package.markdown(record), encoding="utf-8")
    s = record["summary"]
    print(f"capd: {record['gate']} package: {s['present']} present, {s['missing']} missing, {s['na']} N/A, "
          f"{s['workbookErrors']} workbook error(s); record {record['recordSha256'][:16]} written to {out}")
    return 0 if s["complete"] else 1


def cmd_mapping(args) -> int:
    from . import mapping

    records = mapping.load(args.path)
    if args.action == "views":
        print(mapping.views(records), end="")
        return 0
    result = mapping.check(records)
    print(json.dumps(result, indent=1))
    return 0


def cmd_catalog(args) -> None:
    cat = Catalog.load()
    if args.key:
        print(json.dumps(cat.get(args.key), indent=1))
        return
    if args.search:
        q = args.search.lower()
        for r in cat.rules.values():
            if q in (r["title"] + " " + r.get("text", "") + " " + r["sourceId"]).lower():
                print(f"{r['key']:<20} {r['sourceId']:<8} {r['title'][:90]}")
        return
    print(json.dumps(cat.summary(), indent=1))


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="capd", description="Continuous APD certification toolkit")
    p.add_argument("--version", action="version", version=f"capd {__version__}")
    sub = p.add_subparsers(dest="command", required=True)

    def build_flags(sp):
        sp.add_argument("--build-id"), sp.add_argument("--commit"), sp.add_argument("--branch")
        sp.add_argument("--pull-request"), sp.add_argument("--environment")

    def source_flags(sp):
        for f in ("junit", "cucumber", "sarif", "axe"):
            sp.add_argument(f"--{f}", nargs="+", help=f"{f} report paths or globs (in addition to configured sources)")

    sp = sub.add_parser("run", help="collect, check tags, compare, report, and publish in one step")
    sp.add_argument("--config", default="capd.yaml"), sp.add_argument("--baseline", help="evidence bundle from the last main build")
    sp.add_argument("--out-dir", default="out"), sp.add_argument("--report-url"), sp.add_argument("--no-publish", action="store_true")
    sp.add_argument("--dry-run", action="store_true", help="sinks show what they would send")
    build_flags(sp), source_flags(sp)

    sp = sub.add_parser("collect", help="read test reports and scans into an evidence bundle")
    sp.add_argument("--config"), sp.add_argument("-o", "--out", default="out/bundle.json")
    build_flags(sp), source_flags(sp)

    sp = sub.add_parser("check-tags", help="lint rule tags")
    sp.add_argument("--bundle", default="out/bundle.json"), sp.add_argument("--config")

    sp = sub.add_parser("compare", help="the pull request gate: compare with the last main build")
    sp.add_argument("--bundle", default="out/bundle.json"), sp.add_argument("--baseline"), sp.add_argument("--config")
    sp.add_argument("--quarantine"), sp.add_argument("--mode", choices=["report-only", "blocking"])
    sp.add_argument("-o", "--out", default="out/comparison.json"), sp.add_argument("--markdown", default="out/summary.md")
    sp.add_argument("--report-url")

    sp = sub.add_parser("report", help="write the static HTML report")
    sp.add_argument("--bundle", default="out/bundle.json"), sp.add_argument("--comparison", default="out/comparison.json")
    sp.add_argument("-o", "--out", default="out/report.html"), sp.add_argument("--title", default="Certification readiness report")

    sp = sub.add_parser("publish", help="run the configured sink connectors")
    sp.add_argument("--config", default="capd.yaml"), sp.add_argument("--bundle", default="out/bundle.json")
    sp.add_argument("--comparison", default="out/comparison.json"), sp.add_argument("--report-url")
    sp.add_argument("--only", nargs="+"), sp.add_argument("--dry-run", action="store_true")
    build_flags(sp)

    sp = sub.add_parser("validate", help="validate agency files, pinned templates, or golden test cases")
    sp.add_argument("what", choices=["orw", "intake", "sirt", "templates", "cases"])
    sp.add_argument("path", nargs="?"), sp.add_argument("--module", default="ee"), sp.add_argument("--config")
    sp.add_argument("--bundle", help="sirt: an evidence bundle, to warn on Y answers whose tagged tests fail")

    sp = sub.add_parser("package", help="check a gate package folder and write a hashed submission record")
    sp.add_argument("action", choices=["check", "verify"])
    sp.add_argument("target", help="check: the gate (ORR, CR, FNA-UAT, FNA-PILOT); verify: a submission-record.json")
    sp.add_argument("dir", nargs="?", help="the package folder (for verify, optional: also re-hash the files)")
    sp.add_argument("--bundle", help="evidence bundle, linked into the record and used by the SIRT check")
    sp.add_argument("--config"), sp.add_argument("-o", "--out", default="out/package")

    sp = sub.add_parser("mapping", help="turn mapping.yaml into metric-contract views, or check what it covers")
    sp.add_argument("action", choices=["views", "check"]), sp.add_argument("path")

    sp = sub.add_parser("catalog", help="show the rules catalog")
    sp.add_argument("--key"), sp.add_argument("--search")

    sub.add_parser("connectors", help="list installed connectors")
    return p


def main(argv=None) -> int:
    args = parser().parse_args(argv)
    try:
        if args.command == "run":
            return cmd_run(args)
        if args.command == "collect":
            cmd_collect(args)
        elif args.command == "check-tags":
            return cmd_check_tags(args)
        elif args.command == "compare":
            return cmd_compare(args)
        elif args.command == "report":
            cmd_report(args)
        elif args.command == "publish":
            cmd_publish(args)
        elif args.command == "validate":
            return cmd_validate(args)
        elif args.command == "package":
            return cmd_package(args)
        elif args.command == "mapping":
            return cmd_mapping(args)
        elif args.command == "catalog":
            cmd_catalog(args)
        elif args.command == "connectors":
            for name, ref in sorted(connectors.available().items()):
                print(f"{name:<14} {ref}")
    except (ValueError, KeyError, FileNotFoundError) as exc:
        print(f"capd: error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
