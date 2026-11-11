"""Validate a state's SIRT response workbook against the pinned FNA template and the catalog.

The SNAP System Integrity Review Tool (SIRT) is an Excel workbook. The state answers each row before UAT.
Checks:
- the workbook follows the pinned template version (sheet names and header rows);
- no rows were added, removed, or moved (each catalog row still holds its SIRT ID);
- every row has an answer (Y, N, or NA in the Y/N columns; the FNS report rows need a frequency,
  data source, or comment);
- every "N" answer gives a reason ("If no, why?", or the comment where the sheet has no reason column);
- with an evidence bundle: a "Y" answer on a rule whose tagged tests fail is a warning.
"""

from __future__ import annotations

from pathlib import Path

from .templates import SIRT_SHEETS, fingerprint, known_fingerprints, open_workbook

YES, NO, NA = {"Y", "YES"}, {"N", "NO"}, {"NA", "N/A"}
HEADER_FIRST = {"ID", "Report"}


def _clean(v) -> str:
    return " ".join(str(v).split()) if v is not None else ""


def _header_for(ws, row: int) -> list[str]:
    """The nearest header row at or above `row` (the Reporting sheet has a second header for FNS reports)."""
    for r in range(row, 0, -1):
        first = _clean(ws.cell(r, 1).value)
        if first in HEADER_FIRST:
            return [_clean(c.value) for c in ws[r]]
    return [_clean(c.value) for c in ws[1]]


def _columns(header: list[str]) -> tuple[list[int], int | None, int | None]:
    answers = [i for i, h in enumerate(header) if "Y/N" in h or h.endswith("System")]
    free = not answers
    if free:  # FNS report rows: frequency and data source instead of Y/N
        answers = [i for i, h in enumerate(header) if h in ("Frequency", "Data Source")]
    reason = next((i for i, h in enumerate(header) if h.startswith("If no")), None)
    comment = next((i for i, h in enumerate(header) if h.startswith("Comment")), None)
    return answers, reason if reason is not None else comment, comment if free else None


def failing_rules(bundle: dict) -> set[str]:
    """Rules with at least one failing tagged test in the bundle."""
    return {k for r in bundle["records"] if r["kind"] == "test" and r["result"] == "fail" for k in r["ruleIds"]}


def validate(path: str | Path, catalog, bundle: dict | None = None) -> dict:
    wb = open_workbook(path)
    fp = fingerprint(wb, SIRT_SHEETS)
    known = known_fingerprints()
    if fp not in known:
        return {"file": str(path), "template": None, "answered": 0, "rows": 0,
                "errors": [f"unknown SIRT template version (fingerprint {fp}); refusing to validate"], "warnings": []}
    errors: list[str] = []
    warns: list[str] = []
    failing = failing_rules(bundle) if bundle else set()
    rules = sorted((r for r in catalog.rules.values() if r["set"] == "sirt" and r["agency"] == "fna"),
                   key=lambda r: r["key"])
    answered = 0
    for r in rules:
        sheet, row = r["source"]["sheet"], r["source"]["row"]
        ws = wb[sheet]
        where = f"{sheet} row {row} ({r['sourceId']}, {r['key']})"
        if not _clean(ws.cell(row, 1).value).startswith(r["sourceId"]):
            errors.append(f"{where}: expected SIRT ID {r['sourceId']} but found "
                          f"'{_clean(ws.cell(row, 1).value)}'; rows were added, removed, or moved")
            continue
        header = _header_for(ws, row)
        answer_cols, reason_col, free_col = _columns(header)
        values = [_clean(ws.cell(row, c + 1).value).upper() for c in answer_cols]
        free_text = _clean(ws.cell(row, free_col + 1).value) if free_col is not None else ""
        if not any(values) and not free_text:
            errors.append(f"{where}: no answer")
            continue
        answered += 1
        if free_col is not None:
            continue
        for v in values:
            if v and v not in YES | NO | NA:
                warns.append(f"{where}: unexpected answer '{v}' (use Y, N, or NA)")
        if any(v in NO for v in values) and (reason_col is None or not _clean(ws.cell(row, reason_col + 1).value)):
            errors.append(f"{where}: answered N without a reason in '{header[reason_col] if reason_col is not None else 'Comment/Response'}'")
        if any(v in YES for v in values) and r["key"] in failing:
            warns.append(f"{where}: answered Y, but tagged tests for this rule fail in the evidence bundle")
    return {"file": str(path), "template": known[fp], "rows": len(rules), "answered": answered,
            "errors": errors, "warnings": warns}
