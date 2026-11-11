"""Validate an SMC Intake Form against the pinned template and the catalog.

Checks: known template version, every CEF listed, every CMS-required outcome for the module listed,
N/A rows justified in the comments, and state-specific outcome references in the Intake Form format
(ST + module + two digits, for example STEE01).
"""

from __future__ import annotations

import re
from pathlib import Path

from .templates import INTAKE_SHEETS, fingerprint, headers, known_fingerprints, open_workbook

STATE_REF = re.compile(r"^ST[A-Z]+\d{2,}$")


def _rows(ws):
    for i, row in enumerate(ws.iter_rows(min_row=3, values_only=True), start=3):
        if any(v not in (None, "") for v in row):
            yield i, list(row)


def validate(path: str | Path, catalog, module: str = "ee") -> dict:
    wb = open_workbook(path)
    errors: list[str] = []
    fp = fingerprint(wb, INTAKE_SHEETS)
    known = known_fingerprints()
    if fp not in known:
        return {"file": str(path), "template": None,
                "errors": [f"unknown Intake Form template version (fingerprint {fp}); refusing to validate"], "warnings": []}

    cef = wb["Conditions for Enhanced Funding"]
    hc = headers(cef)
    seen_cef = set()
    for i, row in _rows(cef):
        ref = str(row[0]).strip()
        if ref.isdigit():
            seen_cef.add(f"CEF{int(ref):02d}")
        elif ref.upper().startswith("CEF"):
            seen_cef.add(ref.upper().replace(" ", ""))
        _check_na(errors, "Conditions for Enhanced Funding", i, row, hc)
    for r in catalog.rules.values():
        if r["set"] == "cef" and r["sourceId"] not in seen_cef:
            errors.append(f"Conditions for Enhanced Funding: {r['sourceId']} is missing (all 22 CEF must be listed)")

    om = wb["Outcomes & Metrics"]
    ho = headers(om)
    seen = set()
    for i, row in _rows(om):
        ref = str(row[0] or "").split()[0].strip() if row[0] else ""
        if not ref:
            continue
        seen.add(ref)
        if ref.startswith("ST") and not STATE_REF.match(ref):
            errors.append(f"Outcomes & Metrics row {i}: state-specific reference '{ref}' must look like ST{module.upper()}01")
        _check_na(errors, "Outcomes & Metrics", i, row, ho)
    required = [r["sourceId"] for r in catalog.rules.values() if r["agency"] == "cms" and r["set"] == module and r.get("applicable", True)]
    for sid in required:
        if sid not in seen:
            errors.append(f"Outcomes & Metrics: CMS-required outcome {sid} is missing")
    return {"file": str(path), "template": known[fp], "errors": errors, "warnings": []}


def _check_na(errors, sheet, i, row, hdr):
    for ev in ("State ORR Evidence", "State CR Evidence"):
        if ev in hdr and str(row[hdr.index(ev)] or "").strip().upper() == "N/A":
            cm = ev.replace("Evidence", "Comments")
            if cm not in hdr or not str(row[hdr.index(cm)] or "").strip():
                errors.append(f"{sheet} row {i}: '{ev}' is N/A without a justification in '{cm}'")
