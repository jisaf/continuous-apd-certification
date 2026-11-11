# Notices and sources

The rules, examples, and research in this project are derived from the following public sources. U.S. government works are in the public domain in the United States (17 U.S.C. § 105). Agency documents remain authoritative; this project may lag behind or misread them.

## Centers for Medicare & Medicaid Services (CMS)

- [Streamlined Modular Certification Guidance, v2.0](https://www.medicaid.gov/medicaid/data-and-systems/downloads/smc-certification-guidance.pdf)
- [MES Certification Repository](https://cmsgov.github.io/CMCS-DSG-DSS-Certification/) ([source](https://github.com/CMSgov/CMCS-DSG-DSS-Certification)) — CMS-required outcomes, default metrics, Conditions for Enhanced Funding, and templates. *As of 2026-11-11 that repository's license file contains only a placeholder ("This is probably in the public domain, but CMMS needs to put their license here."). We treat its content as a U.S. government work and credit it here.*
- [MES Testing Guidance Framework](https://www.medicaid.gov/medicaid/data-and-systems/downloads/mes-testing-guidance-framework.pdf)
- [State Health Official letter #25-003](https://www.medicaid.gov/federal-policy-guidance/downloads/sho25003.pdf), August 6, 2025 — new MES templates
- [Acceptable Risk Controls for ACA, Medicaid, and Partner Entities (ARC-AMPE), Volume I v1.02](https://www.cms.gov/files/document/arc-ampe-vol-1-v102-508-5cr-04112025.pdf), April 10, 2025 — the CMS security and privacy framework that "supersedes and replaces MARS-E" for ACA Administering Entities, including state Medicaid agencies. *Note: as of 2026-11-11 the MES Certification Repository's Planning page still refers to MARS-E; we follow ARC-AMPE.*
- [Hospital Price Transparency tools](https://cmsgov.github.io/hpt-tool/) — design inspiration only; no code is used

## USDA Food and Nutrition Administration (FNA, formerly FNS)

- [FNS Handbook 901 v2.5](https://www.usda.gov/sites/default/files/guidance-documents/fns-handbook901-version2.5.pdf), updated 2025-12-11 ([handbook page](https://www.fna.usda.gov/sso/apd/handbook-901))
- [SNAP System Integrity Review Tool (SIRT)](https://www.fna.usda.gov/snap/system-integrity-review-tool). The Excel version is included unchanged as `src/capd/data/fna_templates/sirt-template.xlsx` (retrieved 2026-11-11, SHA-256 `3807540101a44b334db75f7d7350b9819faba552d055299b7ce2dd200fee8249`) so the SIRT response check can recognize it. The filled sample in `examples/sample-package/` is fictional.
- [SNAP Eligibility System Go Live Requirements](https://www.fna.usda.gov/sso/snap-eligibility-system-golive-requirements), December 2023
- [Final Rule: System Testing, 7 CFR 277.18](https://www.fna.usda.gov/sso/fr-010214a)

## Community projects

- [MES Certification Navigator](https://github.com/jeff-prov-adv/mes-navigator) by Provenance Advisors (MIT License; unofficial). Its pinned-upstream model informs our catalog maintenance. If we reuse any of its code, its MIT notice will be kept with that code.

## Sample system and golden cases

- [18F SNAP API prototype](https://github.com/18F/snap-api-prototype) (commit 215f3f3b, 2020-08-17). A U.S. government
  work with a CC0 1.0 waiver. Its benefit calculator is included unchanged in `examples/sample-system/vendor/`
  (see `LICENSE-18F.md` there) as the demo's stand-in system, and its Gherkin scenarios are converted into the
  golden cases in `examples/golden-cases/snap/`. Expected values are 18F's FY2020 results.

