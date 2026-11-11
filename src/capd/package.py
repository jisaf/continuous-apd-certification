"""Gate package check and hashed submission record.

A gate package is the folder of files a state sends to CMS or FNA for a review (letters, plans, the
agency workbooks). `capd package` checks the folder against the catalog and writes a submission record:

- a checklist of every applicable rule for the gate that rests on a file (a document, an attestation,
  a demonstration record, or a report), marked present, missing, or N/A;
- the agency workbooks the gate needs (SMC Intake Form, ORW, SIRT response), each checked by its validator;
- the SHA-256 of every file in the folder, and a hash over the whole record.

It tracks files only. It does not judge their content (except the workbook checks), and tests and
metrics stay with the pipeline and the report layer.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import yaml

from . import SCHEMA_VERSION, __version__, schemas
from .evidence import load as load_bundle
from .evidence import now_iso

FILE_KINDS = {"document", "attestation", "demonstration", "report"}
# Workbooks each gate needs by default. A package index can change this with `workbooks:`.
DEFAULT_WORKBOOKS = {"ORR": ["intake"], "CR": ["intake", "orw"], "FNA-UAT": ["sirt"], "FNA-PILOT": []}
WORKBOOK_NAMES = {"intake": "SMC Intake Form", "orw": "Operational Report Workbook (ORW)",
                  "sirt": "SIRT response workbook"}
INDEX = "package.yaml"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def checklist_rules(catalog, gate: str) -> list[dict]:
    """Rules for the gate that rest on a file. SIRT rows are answered in the SIRT workbook, not as files."""
    out = []
    for r in catalog.rules.values():
        kinds = set(r.get("gates", {}).get(gate, []))
        if kinds & FILE_KINDS and r["set"] != "sirt":
            out.append(r)
    return sorted(out, key=lambda r: r["key"])


def _validate_workbook(kind: str, path: Path, catalog, bundle) -> dict:
    from .validators import intake, orw, sirt

    if kind == "orw":
        return orw.validate(path)
    if kind == "intake":
        return intake.validate(path, catalog)
    return sirt.validate(path, catalog, bundle)


def build(directory: str | Path, gate: str, catalog, bundle_path: str | None = None) -> dict:
    from .validators import templates

    root = Path(directory)
    if not root.is_dir():
        raise FileNotFoundError(f"package folder not found: {root}")
    index = yaml.safe_load((root / INDEX).read_text()) if (root / INDEX).exists() else {}
    index = index or {}
    if index.get("gate") and index["gate"] != gate:
        raise ValueError(f"{root / INDEX} is for gate {index['gate']}, not {gate}")
    items: dict[str, list[str]] = {k: list(v or []) for k, v in (index.get("items") or {}).items()}
    for key in items:
        if key not in catalog:
            raise ValueError(f"{INDEX}: unknown rule key '{key}'")
    bundle = load_bundle(bundle_path) if bundle_path else None

    files = []
    found_workbooks: dict[str, list[str]] = {}
    for p in sorted(x for x in root.rglob("*") if x.is_file() and x.name != INDEX):
        rel = p.relative_to(root).as_posix()
        entry = {"path": rel, "sha256": sha256_file(p), "bytes": p.stat().st_size,
                 "rules": sorted(k for k, v in items.items() if rel in v)}
        if p.suffix.lower() == ".xlsx":
            kind = templates.identify(p)
            if kind:
                entry["template"] = kind
                found_workbooks.setdefault(kind, []).append(rel)
        files.append(entry)
    present = {f["path"] for f in files}

    checklist = []
    for r in checklist_rules(catalog, gate):
        listed = items.get(r["key"], [])
        missing_files = [f for f in listed if f not in present]
        if not r.get("applicable", True):
            status = "na"
        elif listed and not missing_files:
            status = "present"
        else:
            status = "missing"
        row = {"key": r["key"], "sourceId": r["sourceId"], "title": r["title"], "owner": r["responsibility"],
               "kinds": sorted(set(r["gates"][gate]) & FILE_KINDS), "status": status, "files": listed}
        if missing_files:
            row["missingFiles"] = missing_files
        checklist.append(row)

    workbooks = []
    for kind in index.get("workbooks", DEFAULT_WORKBOOKS.get(gate, [])):
        paths = found_workbooks.get(kind, [])
        if not paths:
            workbooks.append({"kind": kind, "name": WORKBOOK_NAMES[kind], "file": None,
                              "errors": [f"no {WORKBOOK_NAMES[kind]} in the package"], "warnings": []})
        for rel in paths:
            res = _validate_workbook(kind, root / rel, catalog, bundle)
            workbooks.append({"kind": kind, "name": WORKBOOK_NAMES[kind], "file": rel,
                              "errors": res["errors"], "warnings": res["warnings"]})

    counts = {s: sum(1 for c in checklist if c["status"] == s) for s in ("present", "missing", "na")}
    record = {
        "schemaVersion": SCHEMA_VERSION,
        "gate": gate,
        "createdAt": now_iso(),
        "capdVersion": __version__,
        "catalogVersion": catalog.version,
        "summary": {**counts, "workbookErrors": sum(len(w["errors"]) for w in workbooks),
                    "complete": counts["missing"] == 0 and all(not w["errors"] for w in workbooks)},
        "checklist": checklist,
        "workbooks": workbooks,
        "files": files,
    }
    if bundle:
        record["evidenceBundle"] = {"build": bundle["build"].get("id", ""), "recordsSha256": bundle["recordsSha256"]}
    record["recordSha256"] = hashlib.sha256(json.dumps(record, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    schemas.check("submission-record", record)
    return record


def verify(record: dict, directory: str | Path | None = None) -> list[str]:
    """Check a saved record: its own hash, and (with a folder) that every file still has the recorded hash."""
    problems = []
    body = {k: v for k, v in record.items() if k != "recordSha256"}
    if hashlib.sha256(json.dumps(body, sort_keys=True, separators=(",", ":")).encode()).hexdigest() != record["recordSha256"]:
        problems.append("recordSha256 does not match the record (the record was changed)")
    if directory is not None:
        root = Path(directory)
        for f in record["files"]:
            p = root / f["path"]
            if not p.exists():
                problems.append(f"{f['path']}: missing")
            elif sha256_file(p) != f["sha256"]:
                problems.append(f"{f['path']}: changed since the record was made")
    return problems


def markdown(record: dict) -> str:
    s = record["summary"]
    lines = [f"# {record['gate']} package checklist", "",
             f"Catalog {record['catalogVersion']} · capd {record['capdVersion']} · {record['createdAt']} · "
             f"record `{record['recordSha256'][:16]}`", "",
             f"**{'Complete' if s['complete'] else 'Not complete'}:** {s['present']} present, {s['missing']} missing, "
             f"{s['na']} N/A; {s['workbookErrors']} workbook error(s).", "",
             "This checklist covers files only. Tests and metrics come from the pipeline and the report layer.", "",
             "## Agency workbooks", ""]
    for w in record["workbooks"]:
        mark = "OK" if not w["errors"] else f"{len(w['errors'])} error(s)"
        lines.append(f"- **{w['name']}** ({w['file'] or 'not found'}): {mark}"
                     + (f", {len(w['warnings'])} warning(s)" if w["warnings"] else ""))
        for e in w["errors"][:10]:
            lines.append(f"  - {e}")
        if len(w["errors"]) > 10:
            lines.append(f"  - ... and {len(w['errors']) - 10} more (see submission-record.json)")
    lines += ["", "## Files the gate needs", "", "| Status | Rule | Item | Owner | Files |", "| --- | --- | --- | --- | --- |"]
    order = {"missing": 0, "present": 1, "na": 2}
    for c in sorted(record["checklist"], key=lambda c: (order[c["status"]], c["key"])):
        lines.append(f"| {c['status']} | `{c['key']}` | {c['title'][:80]} | {c['owner']} | {', '.join(c['files']) or '-'} |")
    lines += ["", "## File hashes (SHA-256)", ""]
    lines += [f"- `{f['sha256']}` {f['path']}" for f in record["files"]] or ["- (no files)"]
    return "\n".join(lines) + "\n"
