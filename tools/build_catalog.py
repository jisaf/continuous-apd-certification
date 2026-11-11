"""Build the rules catalog (src/capd/data/catalog/catalog.json) from pinned sources.

Inputs (all public-domain U.S. government content or CC0 research in this repository):
  catalog/sources/cms-required-ee.csv   CMS MES Certification Repository, CMS-required E&E outcomes
  catalog/sources/cms-cefs.csv          CMS MES Certification Repository, Conditions for Enhanced Funding
  docs/research/classification/*.csv   row-by-row evidence classification (E&E, CEF, SIRT, Go Live)

Run:  python tools/build_catalog.py
The output is deterministic, so a rebuild with unchanged inputs produces an identical file.
Rule keys never change once published. SIRT keys (fna:sirt:S0001...) follow the order of the
SIRT Excel rows at catalog version 1.0.0; later FNA renumbering is handled by the change log.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / "catalog" / "sources"
CLASS = ROOT / "docs" / "research" / "classification"
OUT = ROOT / "src" / "capd" / "data" / "catalog" / "catalog.json"

CATALOG_VERSION = "1.0.0"
CMS_REPO_COMMIT = "c9db9cd049f6641373b1ad0bb5aa1e07bd0ce68a"
CMS_REPO = "https://github.com/CMSgov/CMCS-DSG-DSS-Certification"
SIRT_URL = "https://www.fna.usda.gov/snap/system-integrity-review-tool"
GOLIVE_URL = "https://www.fna.usda.gov/sso/snap-eligibility-system-golive-requirements"

KIND = {
    "AUTO_TEST": "test",
    "DATA_METRIC": "metric",
    "REPORT_CHECK": "report",
    "MANUAL_DEMO": "demonstration",
    "DOCUMENT": "document",
    "EXTERNAL": "attestation",
}
RESPONSIBILITY = {
    "test": "vendor",
    "report": "vendor",
    "metric": "shared",
    "demonstration": "shared",
    "document": "state",
    "attestation": "third_party",
}
FRESHNESS_DAYS = {
    "test": 30,
    "report": 30,
    "metric": 45,
    "demonstration": 180,
    "document": 365,
    "attestation": 365,
}
ACCEPTANCE_REQUIRED = {"document", "attestation", "demonstration"}
# Coverage: "evidenced" when the toolkit produces or checks the evidence itself.
EVIDENCED = {"test", "metric"}
MULTI_PROGRAM = {"EE21"}  # outcomes that span Medicaid and SNAP in an integrated system


def kinds(code: str) -> list[str]:
    out: list[str] = []
    for part in (code or "").split("+"):
        part = part.strip()
        if part and KIND[part] not in out:
            out.append(KIND[part])
    return out


def rule(key, agency, rset, source_id, title, text, citations, gates, primary_kind, source, **extra):
    programs = ["medicaid"] if agency == "cms" else ["snap"]
    if source_id in MULTI_PROGRAM:
        programs = ["medicaid", "snap"]
    entry = {
        "key": key,
        "agency": agency,
        "set": rset,
        "sourceId": source_id,
        "title": title,
        "text": text,
        "citations": citations,
        "programs": programs,
        "gates": gates,
        "responsibility": RESPONSIBILITY[primary_kind],
        "coverage": "evidenced" if primary_kind in EVIDENCED else "tracked_only",
        "acceptance": "required" if primary_kind in ACCEPTANCE_REQUIRED else "not_required",
        "freshnessDays": FRESHNESS_DAYS[primary_kind],
        "source": source,
    }
    entry.update(extra)
    return entry


def read_csv(path: Path) -> list[dict]:
    with path.open(encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def ee_rules() -> list[dict]:
    cms = {r["Reference #"].split()[0].strip(): r for r in read_csv(SOURCES / "cms-required-ee.csv") if r["Reference #"].strip()}
    out = []
    for c in read_csv(CLASS / "ee_outcomes_classified.csv"):
        sid = c["id"].strip()
        src = cms[sid]
        cites = [x.strip(" -–") for x in re.split(r"\n+", src.get("Regulatory Sources", "")) if x.strip(" -–")]
        primary = KIND[c["primary"]]
        gates = {"ORR": kinds(c["orr_type"]), "CR": kinds(c["cr_type"])}
        out.append(rule(
            f"cms:ee:{sid}", "cms", "ee", sid, c["short_title"], src["CMS Required Outcomes"].strip(), cites, gates, primary,
            {"document": "MES Certification Repository, CMS-Required Outcomes: Eligibility and Enrollment",
             "url": f"{CMS_REPO}/tree/{CMS_REPO_COMMIT}/_data", "version": CMS_REPO_COMMIT},
            defaultMetrics=src["Default Metrics"].strip(),
        ))
    return out


def cef_rules() -> list[dict]:
    cms = {r["Ref #"].strip(): r for r in read_csv(SOURCES / "cms-cefs.csv") if r["Ref #"].strip().startswith("CEF")}
    out = []
    for c in read_csv(CLASS / "cef_classified.csv"):
        sid = c["id"].strip()
        primary = KIND[c["primary"]]
        gate_kinds = kinds(c["primary"] + ("+" + c["secondary"] if c["secondary"] else ""))
        out.append(rule(
            f"cms:cef:{sid}", "cms", "cef", sid, c["condition_short"], cms[sid]["Condition"].strip(),
            ["42 CFR 433.112(b)"], {"ORR": gate_kinds, "CR": gate_kinds}, primary,
            {"document": "MES Certification Repository, Conditions for Enhanced Funding",
             "url": f"{CMS_REPO}/tree/{CMS_REPO_COMMIT}/_data", "version": CMS_REPO_COMMIT},
            exampleEvidence=cms[sid]["Example Evidence"].strip(),
        ))
    return out


def sirt_rules() -> list[dict]:
    out = []
    n = 0
    for c in read_csv(CLASS / "sirt_classified.csv"):
        if c["in_821"] != "yes":
            continue
        n += 1
        primary = KIND[c["primary"]]
        gate_kinds = kinds(c["primary"])
        text = " ".join(c["question"].split())
        out.append(rule(
            f"fna:sirt:S{n:04d}", "fna", "sirt", c["id"].strip(), text[:120], text,
            [c["citation"].strip()] if c["citation"].strip() else [], {"FNA-UAT": gate_kinds, "FNA-PILOT": gate_kinds}, primary,
            {"document": "SNAP System Integrity Review Tool (Excel)", "url": SIRT_URL, "version": "2023-01-05",
             "sheet": c["sheet"], "row": int(c["row"])},
            prewrite=c["prewrite_candidate"] == "yes",
            textSha256=hashlib.sha256(text.encode()).hexdigest()[:16],
        ))
    return out


def golive_rules() -> list[dict]:
    out = []
    for c in read_csv(CLASS / "golive_classified.csv"):
        primary = KIND[c["primary"]]
        gate_kinds = kinds(c["primary"] + ("+" + c["secondary"] if c["secondary"] else ""))
        out.append(rule(
            f"fna:golive:{c['id']}", "fna", "golive", c["id"], c["criterion"], c["criterion"],
            ["SNAP Eligibility System Go Live Requirements (2023)"], {"FNA-UAT": gate_kinds, "FNA-PILOT": gate_kinds}, primary,
            {"document": "SNAP Eligibility System Go Live Requirements", "url": GOLIVE_URL, "version": "2023-12-15"},
        ))
    return out


INDICATORS = [
    {"key": "indicator:golden-cases", "title": "Golden case pass rate",
     "supports": ["cms:ee:EE4", "cms:ee:EE16"], "kind": "test",
     "note": "Directional only: rule correctness, not a PERM or SNAP QC error rate."},
    {"key": "indicator:accessibility-scan", "title": "Automated WCAG 2.2 AA scan",
     "supports": ["cms:cef:CEF12"], "kind": "scan",
     "note": "Automated tools find only part of WCAG issues; manual testing is still required."},
    {"key": "indicator:security-scan", "title": "Static and dependency security scans",
     "supports": ["cms:cef:CEF09", "cms:cef:CEF12"], "kind": "scan",
     "note": "Does not replace the independent third-party assessment."},
]


def build() -> dict:
    rules = ee_rules() + cef_rules() + sirt_rules() + golive_rules()
    keys = [r["key"] for r in rules]
    assert len(keys) == len(set(keys)), "duplicate rule keys"
    return {
        "catalogVersion": CATALOG_VERSION,
        "keySyntax": "<agency>:<set>:<id>",
        "gates": ["ORR", "CR", "FNA-UAT", "FNA-PILOT"],
        "sources": {"cmsRepository": {"url": CMS_REPO, "commit": CMS_REPO_COMMIT},
                    "sirt": {"url": SIRT_URL}, "goLive": {"url": GOLIVE_URL}},
        "indicators": INDICATORS,
        "rules": rules,
    }


def main() -> None:
    catalog = build()
    rules = catalog["rules"]
    OUT.write_text(json.dumps(catalog, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    by_set: dict[str, int] = {}
    for r in rules:
        by_set[r["set"]] = by_set.get(r["set"], 0) + 1
    print(f"wrote {OUT.relative_to(ROOT)}: {len(rules)} rules {by_set}")


if __name__ == "__main__":
    main()
