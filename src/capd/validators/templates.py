"""Pinned CMS templates and fingerprints. Generators and validators refuse template versions they do not know."""

from __future__ import annotations

import hashlib
import warnings
from importlib import resources

import openpyxl

PINNED = {
    "orw": ("capd.data.cms_templates", "orw-template.xlsx"),
    "orw-validation": ("capd.data.cms_templates", "orw-validation.xlsx"),
    "intake": ("capd.data.cms_templates", "intake-form-template.xlsx"),
    "sirt": ("capd.data.fna_templates", "sirt-template.xlsx"),
}
SOURCE = {"repository": "https://github.com/CMSgov/CMCS-DSG-DSS-Certification",
          "commit": "c9db9cd049f6641373b1ad0bb5aa1e07bd0ce68a"}
SIRT_SOURCE = {"url": "https://www.fna.usda.gov/sites/default/files/resource-files/SNAP_System_Integrity_Review_Tool_Excel.xlsx",
               "sha256": "3807540101a44b334db75f7d7350b9819faba552d055299b7ce2dd200fee8249",
               "retrieved": "2026-11-11"}


def open_workbook(path):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return openpyxl.load_workbook(path)


def pinned_path(name: str):
    package, filename = PINNED[name]
    return resources.files(package).joinpath(filename)


def headers(ws) -> list[str]:
    row = next(ws.iter_rows(min_row=1, max_row=1, values_only=True), ())
    return [str(c).strip() for c in row if c is not None]


def fingerprint(wb, sheets: list[str]) -> str:
    """Hash of sheet names and their header rows: identifies a template version independent of content."""
    parts = []
    for name in sheets:
        if name in wb.sheetnames:
            parts.append(name + "|" + "|".join(headers(wb[name])))
        else:
            parts.append(name + "|<missing>")
    return hashlib.sha256("\n".join(parts).encode()).hexdigest()[:16]


ORW_SHEETS = ["Metric Definitions", "Metric Values"]
INTAKE_SHEETS = ["Conditions for Enhanced Funding", "Outcomes & Metrics"]
SIRT_SHEETS = ["Eligibility (A and B)", "Claims (C)", "Notices (D)", "Operations (E and F)",
               "Reporting (E10 & E13)", "Data Match (E11 & E12)"]


def known_fingerprints() -> dict[str, str]:
    with resources.as_file(pinned_path("orw")) as p:
        orw = fingerprint(open_workbook(p), ORW_SHEETS)
    with resources.as_file(pinned_path("intake")) as p:
        intake = fingerprint(open_workbook(p), INTAKE_SHEETS)
    with resources.as_file(pinned_path("sirt")) as p:
        sirt = fingerprint(open_workbook(p), SIRT_SHEETS)
    return {orw: "CMS ORW template (MES Certification Repository @ c9db9cd)",
            intake: "CMS SMC Intake Form, Appendix E template (MES Certification Repository @ c9db9cd)",
            sirt: "FNA SNAP System Integrity Review Tool, Excel version (retrieved 2026-11-11)"}


def identify(path) -> str | None:
    """Which pinned template a workbook follows: 'orw', 'intake', 'sirt', or None."""
    wb = open_workbook(path)
    for kind, sheets in (("orw", ORW_SHEETS), ("intake", INTAKE_SHEETS), ("sirt", SIRT_SHEETS)):
        if all(s in wb.sheetnames for s in sheets) and fingerprint(wb, sheets) in known_fingerprints():
            return kind
    return None


def orw_rules_conformance() -> list[str]:
    """Compare the pinned ORW template with the pinned ORW_Validation.xlsx. Returns the disagreements."""
    with resources.as_file(pinned_path("orw")) as p:
        tpl = open_workbook(p)
    with resources.as_file(pinned_path("orw-validation")) as p:
        val = open_workbook(p)
    expected: dict[str, set[str]] = {}
    for row in val.worksheets[0].iter_rows(min_row=2, values_only=True):
        if row and row[0] and row[1]:
            expected.setdefault(str(row[0]).strip(), set()).add(str(row[1]).strip())
    diffs = []
    for sheet, fields in sorted(expected.items()):
        have = set(headers(tpl[sheet])) if sheet in tpl.sheetnames else set()
        for f in sorted(fields - have):
            diffs.append(f"{sheet}: validation rules expect column '{f}', which the template lacks")
        for f in sorted(have - fields):
            diffs.append(f"{sheet}: template has column '{f}', which the validation rules do not describe")
    return diffs
