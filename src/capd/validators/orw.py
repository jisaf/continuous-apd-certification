"""Validate an Operational Report Workbook (ORW) against the pinned CMS template and the ORW rules page.

Rules from the MES Certification Repository "Operational Report Workbook Rules and Guidelines":
no added or renamed columns or tabs, keep the instruction row, no blank rows, no merged cells,
file name ends in _YYYY-MM-DD. Field rules follow ORW_Validation.xlsx where it agrees with the template.
"""

from __future__ import annotations

import re
from datetime import date, datetime
from pathlib import Path

from .templates import ORW_SHEETS, fingerprint, headers, known_fingerprints, open_workbook

FILENAME = re.compile(r"_(\d{4}-\d{2}-\d{2})\.xlsx$")
RECOMMENDED = re.compile(r"^Operational_Workbook_[A-Z]{2}_[A-Z]+_\d{4}-\d{2}-\d{2}\.xlsx$")
VALUE_TYPES = {"Percentage/Ratio", "Numerical", "Yes/No"}
CMS_OUTCOME = re.compile(r"^(EE|CP|DSS/DW|EPS|FM|LTSS|MM|PBM|PDMP|PI|PM|TPL|EVV|CEF)\s?\d+$")
STATE_OUTCOME = re.compile(r"^ST[A-Z/]+\d+$")


def _rows(ws):
    """Data rows: skip header (row 1) and instruction row (row 2). Returns (row number, values)."""
    out = []
    for i, row in enumerate(ws.iter_rows(min_row=3, values_only=True), start=3):
        out.append((i, list(row)))
    while out and all(v in (None, "") for v in out[-1][1]):
        out.pop()
    return out


def validate(path: str | Path) -> dict:
    path = Path(path)
    errors: list[str] = []
    warns: list[str] = []
    if not FILENAME.search(path.name):
        errors.append(f"file name must end in _YYYY-MM-DD.xlsx (got {path.name})")
    elif not RECOMMENDED.match(path.name):
        warns.append("recommended name: Operational_Workbook_[state]_[module]_YYYY-MM-DD.xlsx")
    wb = open_workbook(path)
    fp = fingerprint(wb, ORW_SHEETS)
    known = known_fingerprints()
    if fp not in known:
        errors.append(f"unknown ORW template version (fingerprint {fp}); refusing to validate against a template we do not know")
        return {"file": str(path), "template": None, "errors": errors, "warnings": warns}
    for name in ORW_SHEETS:
        ws = wb[name]
        if ws.merged_cells.ranges:
            errors.append(f"{name}: merged cells are not allowed ({len(ws.merged_cells.ranges)} found)")
        instr = next(ws.iter_rows(min_row=2, max_row=2, values_only=True), ())
        if not any(isinstance(c, str) and c.strip() for c in instr):
            errors.append(f"{name}: the instruction row (row 2) was removed")
        for i, row in _rows(ws):
            if all(v in (None, "") for v in row):
                errors.append(f"{name}: blank row {i} inside the data")

    defs = wb["Metric Definitions"]
    hd = headers(defs)
    col = {h: hd.index(h) for h in hd}
    metric_ids = set()
    for i, row in _rows(defs):
        if all(v in (None, "") for v in row):
            continue
        mid = str(row[col["Metric ID"]] or "").strip()
        if not mid:
            errors.append(f"Metric Definitions row {i}: Metric ID is required")
            continue
        metric_ids.add(mid)
        vtype = str(row[col["Value Type"]] or "").strip()
        if vtype not in VALUE_TYPES:
            errors.append(f"Metric Definitions row {i} ({mid}): Value Type must be one of {sorted(VALUE_TYPES)}")
        refs = [r.strip() for r in str(row[col["Outcome Reference #"]] or "").split("|") if r.strip()]
        if not refs:
            errors.append(f"Metric Definitions row {i} ({mid}): Outcome Reference # is required")
        for r in refs:
            if not (CMS_OUTCOME.match(r) or STATE_OUTCOME.match(r)):
                errors.append(f"Metric Definitions row {i} ({mid}): outcome reference '{r}' is not a CMS outcome (for example EE1) "
                              "or a state-specific outcome in the Intake Form format (for example STEE01)")
        if vtype == "Percentage/Ratio":
            for f in ("Numerator Description", "Denominator Description"):
                if not str(row[col[f]] or "").strip():
                    errors.append(f"Metric Definitions row {i} ({mid}): {f} is required for Percentage/Ratio metrics")

    vals = wb["Metric Values"]
    hv = headers(vals)
    vc = {h: hv.index(h) for h in hv}
    for i, row in _rows(vals):
        if all(v in (None, "") for v in row):
            continue
        month = row[vc["Reporting Month"]]
        if not isinstance(month, (date, datetime)):
            errors.append(f"Metric Values row {i}: Reporting Month must be a date")
        st = str(row[vc["State"]] or "")
        if not re.fullmatch(r"[A-Z]{2}", st):
            errors.append(f"Metric Values row {i}: State must be a two-letter abbreviation")
        mid = str(row[vc["Metric ID"]] or "").strip()
        if mid not in metric_ids:
            errors.append(f"Metric Values row {i}: Metric ID '{mid}' is not defined on Metric Definitions")
        if not isinstance(row[vc["Primary Metric Value"]], (int, float)):
            errors.append(f"Metric Values row {i} ({mid}): Primary Metric Value must be a number")
    return {"file": str(path), "template": known[fp], "errors": errors, "warnings": warns}
