# Golden case set: candidate sources (Medicaid + SNAP E&E, Colorado first)

Research date: 2026-11-11. Public repositories were shallow-cloned and inspected read-only; no downloaded code was run. License claims for the 18F prototypes (U.S. government work plus CC0 waiver), PolicyEngine US (AGPL-3.0), and MAGI in the Cloud (BSD-3, BlueLabs) were re-checked against each repository's license file.
Policy context: FNS is now styled "FNA" on usda.gov pages. The 2025 federal law (H.R. 1, enacted 2025)
changed SNAP ABAWD rules, non-citizen eligibility, SUA/internet costs and more. Any SNAP case dated before FY2026 needs
re-validation before use as a current golden case.

License rule used below:
- US federal government works (18F, USDS, CMS, FNS/FNA, USDA data) = public domain in the US -> can copy into CC0.
- Permissive with notice (BSD/MIT) -> can redistribute, but NOT relabel as CC0; keep in a separate "third-party" folder
  with the notice, or re-derive the case facts independently.
- Copyleft (AGPL, MPL) -> cannot copy into a CC0 set. Can reference by URL/commit, or use the AGPL code in AGPL toolkit code.
  Case facts (numbers) are not copyrightable on their own, but a copied, arranged set is risky; re-derive and cite.
- State works (Colorado HCPF/CDHS): no blanket public-domain rule in Colorado. Treat as "reference and adapt", cite.
- Noncommercial (PolyForm NC) -> incompatible with AGPL and CC0. Do not copy.

---

## 1. PolicyEngine US (rules-as-code, YAML tests) — largest and most current

- URL: https://github.com/PolicyEngine/policyengine-us  (clone HEAD e3dc6b74, last commit 2026-11-11, very active)
- License: GNU AGPL v3 ("GNU AFFERO GENERAL PUBLIC LICENSE Version 3, 19 November 2007"). Tests are in the repo, so AGPL.
- Format: YAML. Each case has `name`, `period`, `input` (people / spm_units / tax_units / households), `output` (expected values).
- Counts (`^- name:` entries under policyengine_us/tests/policy/baseline/):
  - gov/usda/snap: 95 files, 1,227 cases
    - eligibility/work_requirements (ABAWD, general work req, H.R.1 ABAWD, waived areas, good-faith window): 402 cases
    - income/deductions (earned, standard, dependent care, medical, child support, shelter, SUA, heat-and-eat, self-employment): 197 cases
    - also: gross/net income tests, BBCE (categorical eligibility ceiling), max/min allotment, immigration (16-case integration), students,
      ineligible members (22-case integration), emergency allotments, FY2027 COLA
  - gov/hhs/medicaid: 71 files, 1,096 cases
    - eligibility/categories (infant, young child, older child, adult, parent, pregnant, SSI recipient, 209(b), optional senior/disabled,
      working-disabled buy-in): 438 cases
    - long_term_care: 148 cases; medically_needy: 72 cases; emergency Medicaid integration: 22 cases
  - gov/hhs/chip: 177 cases
  - gov/states/co: 107 files, 955 cases (mostly tax). Health/human services subset: co/hcpf (CHP+, OmniSalud) 43 cases;
    co/cdhs (TANF/Colorado Works, LEAP) 166 cases. 154 test files anywhere mention CO as state.
- Expected outputs: yes, every case.
- Weaknesses:
  - Most cases are UNIT tests of one variable with intermediate inputs set directly (for example `snap_net_income: 6_350`),
    not "household facts in -> final determination out". True end-to-end integration cases are few (SNAP integration.yaml: 5 cases).
  - Authority is community. Only ~13 explicit source/URL citations across 1,227 SNAP tests. Expected values were written by developers.
  - No expedited service tests (0 files mention "expedit"). No notices, no renewal/ex parte process tests.
  - Periods: mostly 2025 (420) and 2026 (1,225) for SNAP+Medicaid; some to 2027-2030. So current.
- Sample (gov/usda/snap/eligibility/meets_snap_net_income_test.yaml):
  ```yaml
  - name: Twelve-person Colorado household just above the published FY 2026 net limit fails
    period: 2026-01
    input:
      people:
        person1: {}
      spm_units:
        spm_unit:
          members: [person1]
          snap_unit_size: 12
          snap_net_income: 6_350
      households:
        household:
          members: [person1]
          state_code: CO
    output:
      meets_snap_net_income_test: false
  ```
- Sample (gov/states/co/hcpf/chp/co_chp_eligible.yaml):
  ```yaml
  - name: Too much income
    period: 2023
    input:
      state_code: CO
      is_medicaid_eligible: false
      medicaid_income_level: 2.66
      age: 1
      is_pregnant: false
    output:
      co_chp_eligible: false
  ```
- Note: PolicyEngine's SNAP integration.yaml copies CBPP's worked example ("Family of 3, CBPP Example", source
  https://www.cbpp.org/research/food-assistance/a-quick-guide-to-snap-eligibility-and-benefits). CBPP text is copyrighted;
  facts can be re-derived.
- Use: best oracle and cross-check engine (run our golden cases through PolicyEngine as a second opinion). Do not copy YAML
  into the CC0 set. Re-derive cases and cite file + commit.

## 2. 18F SNAP prototypes (federal, CC0) — small but clean, end-to-end SNAP

- 18F/snap-api-prototype (Python): https://github.com/18F/snap-api-prototype — last commit 2020-08-17 (dormant).
  - License (LICENSE.md): "As a work of the United States government, this project is in the public domain within the
    United States of America. Additionally, we waive copyright and related rights in the work worldwide through the CC0 1.0
    Universal public domain dedication."
  - Gherkin feature files: il.feature 32 scenarios, il-ea.feature 29, vt.feature 2, vt-ea.feature 2, ut.feature 3 = 68 scenarios.
    Plus pytest unit tests (gross income, net income, asset) and a FY2019 SUA table.
- 18F/snap-js-api-prototype (JavaScript): https://github.com/18F/snap-js-api-prototype — last commit 2020-11-12, archived 2021-12-17. Same CC0.
  - il.2020.feature 31, va.2020.feature 23, va.2021.feature 23 = 77 scenarios.
  - Covers: gross/net income tests, BBCE gross limits per state, elderly/disabled (65 mentions), medical deduction, dependent care,
    child support, utility/SUA, emergency allotments. Outputs: eligible yes/no + benefit $ amount.
- Not covered: Colorado, ABAWD, expedited, students, immigration. FY2020/2021 parameters (stale; EA era).
- Format: Gherkin (prose-like, easy to convert to YAML/JSON).
- Sample (snap-api-prototype/features/il-ea.feature):
  ```gherkin
  Scenario: Household (just barely) fails the Gross Income test for IL (165% FPL),
            passes the Net Income Test, is overall ineligible
    Given a 3-person household
    And the household does not include an elderly or disabled member
    And the household has earned income of $3000 monthly
    And the household has other income of $0 monthly
    And the household has assets of $0
    And the household has dependent care costs of $300 monthly
    And the household has rent or mortgage costs of $2000 monthly
    When we run the benefit estimator...
      Then we find the family is likely not eligible
      And we find the estimated benefit is $0 per month
  ```
- Use: copy directly into CC0 set as "historical federal-default" structure templates; recompute expected values for FY2027 + Colorado.

## 3. MAGI in the Cloud (MitC) — HHSIDEAlab/medicaid_eligibility (CMS-adjacent MAGI engine)

- URL: https://github.com/HHSIDEAlab/medicaid_eligibility — last commit 2021-03-31 (dormant). Hosted at medicaideligibilityapi.org.
- Origin (README): built "in partnership with the HHSEntrepeneurs program, BlueLabs, and the State Health Reform Assistance Network".
  "It is not currently used in any federal systems."
- License: BSD 3-clause, "Copyright (c) 2013 BlueLabs LLC". Permissive, needs notice. NOT public domain -> cannot be relabeled CC0.
- Contents:
  - test/fixtures/rule_fixtures/*.rb: 25 rule files, 209 `test_name` cases, each with inputs, state config options, expected_outputs.
    Rules: adult group, child, CHIP eligibility, CHIP waiting period, dependent child covered, emergency Medicaid, former foster care,
    immigration (largest), income, income override, optional targeted low-income children, optional unborn child, parent/caretaker
    relative (+ spouse), pregnant, preliminary Medicaid/CHIP, previously denied, public employee benefits, qualified child,
    referral type, refugee assistance, residency.
  - test/fixtures/*.json: 10 full application JSON fixtures (single mom, 3-generation family, 4-person family, disabled person,
    pregnant foster-care woman, etc.). Only 2 include expected determinations.
  - config/state_config.json: per-state options for ~38 states + default. Colorado NOT listed (falls to default).
- Policy year: 2014-2015 era (FPL tables then). MAGI logic is stable but thresholds are stale.
- Sample (test/fixtures/rule_fixtures/adult_group.rb):
  ```ruby
  {
    test_name: "Applicant Age Under 19 or Above 65",
    inputs: {
      "Medicare Entitlement Indicator" => "Y",
      "Applicant Pregnancy Category Indicator" => "N",
      "Applicant Age" => 13,
      "Applicant Dependent Child Covered Indicator" => "Y"
    },
    configs: { "Option Adult Group" => "Y" },
    expected_outputs: {
      "Applicant Adult Group Category Indicator" => "N",
      "Adult Group Category Ineligibility Reason" => 123
    }
  }
  ```
- Use: good rule-by-rule MAGI category checklist with CMS-style ineligibility reason codes. Redistribute only with BSD notice,
  or re-derive. Also usable as a second oracle (MitC is what USDS used, see #4).

## 4. USDS ene-testing (federal, MitC test generator + renewal scenarios)

- URL: https://github.com/usds/ene-testing — last commit 2024-08-14.
- License: NO LICENSE file. USDS staff work is a US government work (public domain in US), but no explicit CC0 waiver. Low risk; confirm with USDS.
- Contents: generator for MAGI test instances from templates + state config (config_aa.yml, config_nj.yml) + FPL tables.
  test_templates/00001.yml ("Individualized Eligibility 1"), 00002.yml ("Zero Income with Kids"); fuzz_templates 2 renewal scenarios.
  Templates use symbolic incomes (`amount: child_limit-` = just below child limit) -> good boundary-test pattern.
- fuzz.md quotes two ex parte renewal scenarios from Manatt/SHVS "Conducting Eligibility Redeterminations at the Individual
  Level: State Diagnostic Assessment Tool" (Aug 2023; original SHVS URL now 404):
  > "A mother and child are each enrolled in Medicaid on the basis of MAGI, as a household of two, with a MAGI income is 145% of the FPL.
  > The state's MAGI Medicaid threshold is 133% of the FPL for adults and 200% of the FPL for children. The state's separate CHIP
  > eligibility threshold is 250% of the FPL." Expected: "Child renewed automatically; Mother sent for manual renewal".
  Scenario 2: immigrant father + child, 100% FPL -> child renewed automatically, father to manual renewal.
- Key finding in fuzz.md: "the MITC engine does not explicitly support renewals, only applications." Pregnancy/post-partum flags
  flipped many expected outcomes -> shows prose scenarios are under-specified.
- Use: the only published individual-level ex parte renewal golden cases found (2). Pattern for parameterized boundary cases.

## 5. CMS: Income Eligibility Using MAGI Rules (Marketplace training, Oct 2021, CSG-202110)

- URL: https://CMS.gov/marketplace/technical-assistance-resources/income-eligibility-using-magi-rules.pdf
  (older 2020 copy at hhs.gov guidance portal returns 403).
- Federal work, public domain. 2 fully worked multi-person examples with Medicaid/CHIP household vs APTC household, FPL %, and outcome.
- Example #1 (quoted): "George and Louise are married and live in Michigan, which is a Medicaid expansion state. They file a joint
  federal income tax return. They live with their 17-year-old son, Leo, whom they claim as a dependent. George earns $2,000 every month
  as an office manager. At the end of the coverage year, he'll also get a $5,000 bonus. Louise receives $745 each month from Social
  Security Disability Insurance. Leo earned $3,000 from his summer job as a camp counselor."
  Answer: "In Michigan, George and Louise are eligible for APTC and CSRs, and Leo is eligible for Medicaid." Medicaid/CHIP household
  income 150% FPL ($2,745/month, size 3); Leo eligible because child threshold is 160% FPL. APTC household income 172% FPL ($37,940/yr).
- Example #2: unmarried parents, only Karen files and claims Max. Medicaid households differ per person (Karen 2, Bill 2, Max 3 —
  non-filer and child exception rules). Bill 52% FPL -> Medicaid; Max 150% FPL -> Medicaid; Karen 161% -> APTC.
- Use: copy into CC0 set (adapt to Colorado thresholds). Excellent for MAGI household composition (42 CFR 435.603) rules.

## 6. CMS PERM Medicaid/CHIP Eligibility Review Pilots — 100 CMS test cases with state-specific answer keys (NOT public)

- Round 1 Test Case Guidance (release 2014-09-25):
  https://www.cms.gov/research-statistics-data-and-systems/monitoring-programs/medicaid-and-chip-compliance/perm/downloads/round1medicaidandchiptestcasereportingguide1014.pdf
  > "CMS has made available 100 test cases that can be used as part of the Test Case Review. The test cases have been posted to the CALT"
  > "CMS will provide a state-specific 'answer key' of the results for each test case ... found within the Eligibility Outcomes Analysis Tool"
  > "For SBM states, CMS used data consistent with each state's approved state plan (SPAs approved through 7/1/2014)"
- Scenario categories (states run >= 3 cases each): mixed household; non-citizen emergency-only; nuclear family eligible;
  over-income Medicaid & CHIP; non-financial ineligible; reasonable opportunity period; adult 19-64 (expansion states).
  Reporting template also lists "Eligible inmate" and "Citizenship not verified".
- Hosted on CALT (calt.cms.gov, CMS state collaboration site, login only). Colorado (SBM state) should have received a CO answer key.
- Use: ask HCPF/CMS for the 100 cases + Colorado answer key (or FOIA). Would be the highest-authority MAGI golden set if released.
  Federal work -> public domain if obtained.

## 7. CMS scenario taxonomies (no expected outputs)

- "Resources to Support System and Logic Testing for Unwinding when the PHE Ends" (Sept 2022):
  https://www.medicaid.gov/resources-for-states/downloads/resources-support-sys-logic-test-unwinding.pdf
  Scenario types table: age-outs (65+, CHIP age-out, former foster care), household (multiple/no address, tax filing change, mixed
  household, moves, marital change), income (unverifiable, discrepancies, seasonal, no income, switch MAGI <-> non-MAGI),
  pregnancy/postpartum end, immigration status change, incarceration, death data, other coverage. "Can look to PERM audits ...
  to create additional scenarios specific to states".
- FFM Outbound Account Transfer "Scenarios for States, Sample Payloads" (Oct 2022, 3 multi-member use cases as payloads):
  https://www.medicaid.gov/federal-policy-guidance/downloads/ffm-d-trg-outbound-at-scenarios-for-states-overview.pdf
  (not opened; curl blocked). Relevant for account-transfer interface tests.
- PERM ERC household composition fact sheet (findings examples, not test cases):
  https://www.cms.gov/files/document/perm-erc-household-composition-fact-sheet-magi.pdf
- Use: coverage checklist for the golden set; public domain.

## 8. FNA (FNS) SNAP eligibility page — official worked benefit computation (FY2027)

- URL: https://www.fns.usda.gov/snap/recipient/eligibility (redirects to www.fna.usda.gov). Data "Oct. 1, 2026, through Sept. 30, 2027".
- Federal work, public domain.
- One end-to-end example: 4 people, no elderly/disabled, $1,500 earned + $550 Social Security = $2,050 gross (< $3,575 gross limit);
  20% earned deduction $300; standard deduction $217; dependent care $362 -> $1,171 adjusted; half = $585.50; shelter $700 -> excess
  $114.50; net $1,056.50 (< $2,750); 30% = $317 (rounded up); max allotment $1,023 -> "$706, SNAP Allotment for a full month".
- Defect found: the page says "$1,165 - $114.50 = $1,056.50"; the adjusted income is $1,171 (1,171 - 114.50 = 1,056.50). Official
  examples need review too.
- Also gives FY2027 tables: gross/net limits, max allotments, standard deduction $217 (1-3), shelter cap $769, homeless shelter $205.66,
  resource limits $3,000 / $4,750, expedited criteria in prose (< $100 liquid and < $150 gross; or income+resources < shelter).

## 9. FNS Handbook 310 (SNAP QC Review Handbook)

- FY2025 edition (through QC PM 25-01): https://fns-prod.azureedge.us/sites/default/files/resource-files/snap-qc-handbook310-fy25-102924.pdf
  (newer "FNA Handbook 310", Oct 2026, referenced by QC PM 26-06).
- Federal work, public domain. ~230 "example" passages, mostly about QC error determination (variance, error amount, reported vs
  unreported changes, EBT non-use, categorical eligibility proof, household composition, prorating). A few full computations.
- Use: source of edge cases for change reporting, error determination, and categorical eligibility evidence. Not a ready golden set.

## 10. SNAP QC Public Use File (USDA/FNA, Mathematica) — real reviewed households, includes Colorado

- URL: https://snapqcdata.net/datafiles (FY1996-FY2024; FY2024 revised 2026-08-18). CSV, SAS, Stata, SPSS + tech doc.
- FY2024 CSV: 44,891 household records, 1,177 columns; Colorado (STATE=8): 856 records.
- Relevant fields: RAWGROSS, RAWNET, FSERNDED, FSSTDDED, FSDEPDED, FSMEDDED, FSCSDED, SHELDED, HOMELESS_DED, FSTOTDED, FSNETINC,
  RAWBEN, FSBEN, BENMAX, MINIMUM_BEN, CAT_ELIG, EXPEDSER, AMTERR (QC error amount), STATUS.
- No license statement; federal data = public domain.
- Caveat: values are edited for consistency by Mathematica; benefit is the recorded benefit with QC error amount, not a clean
  rules-computed answer. Use as a statistical regression set ("compute benefit from inputs, compare with RAWBEN +/- AMTERR"),
  not as hand-verified golden cases. Only source with real Colorado SNAP households and an expedited-service flag.

## 11. Colorado-specific material

- HCPF "Medical Assistance Renewal Workbook", effective July 2025 for September 2025 renewals:
  https://hcpf.colorado.gov/sites/hcpf/files/2025.07.01%20Renewal%20Workbook%20Final.pdf
  Appendix G has 8+ dated renewal scenarios (manual rescind; automatic and manual reinstatement; resource VCL; renewal packet;
  change in benefit category) with CBMS outcomes AND notices (termination NOA, approval NOA, reinstatement speed letter).
  Sample (Example 2): family of 4 (Mom HCBS, Dad WAwD, two children CHP+), renewal due 11/2025; ex parte 09/01/2025 sends packet +
  VCL for Mom's resources; household returns signature page 10/02/2025 but not VCL; 12/05/2025 worker runs eligibility -> "The mom is
  terminated ... A termination NOA is triggered for the mom ... as of 01/01/2026, she lost coverage. The dad and children receive an
  approval NOA, including their coverage begin date of 12/01/2025".
  No copyright statement found. Colorado state work: reference and adapt, cite.
- Colorado Staff Development Center (training.colorado.gov) desk aids: SNAP Financial Eligibility FY2026 desk aid (parameters, CO max
  shelter $744 FY2026), MAGI self-employment / NOL training with worked MAGI examples (e.g. "-$3,000 SE + $25,000 spouse = $22,000"),
  MAGI household composition desk aid, MBU flowchart, Non-MAGI/LTC income & resource limits, existing vs new case scenarios.
  Many examples spread across documents; no single case library.
- HCPF Eligibility Quality Assurance Case Review Process Manual:
  https://hcpf.colorado.gov/sites/hcpf/files/Eligibility%20Quality%20Assurance%20Case%20Review%20Process%20Manual_1.pdf (not opened).
- CBMS UAT scripts / Deloitte test decks: not public. Would need HCPF/CDHS/OIT request or CORA records request.
- MyFriendBen (Gary Community Ventures, Colorado screener): https://github.com/MyFriendBen/benefits-api — last commit 2026-11-11,
  License: Mozilla Public License 2.0 (file-level copyleft; not CC0-compatible for copying). ~750 test files, uses PolicyEngine for
  SNAP/Medicaid; cross-state tests for MO, WA, KS, NC, NJ, TX, IL; few Colorado SNAP/Medicaid tests (only a CO jeffco student file).
  "validations" are a DB model, not shipped data. Low value for our golden set.

## 12. Other leads checked

- PolicyEngine/policyengine-snapscreener-validation: MIT, last commit 2026-04-27; tests/scenarios.json (114 lines, a handful of
  scenarios) comparing PolicyEngine with snapscreener.com. Minor.
- codeforamerica/safety-net-blueprint: PolyForm Noncommercial 1.0.0 — incompatible. Contains API contracts/state machines, not
  eligibility golden cases.
- Digital Benefits Network / Massive Data Institute "AI-Powered Rules as Code" (2025): LLM evaluation prompts + rubrics for SNAP and
  Medicaid in 7 states; Experiment 3 compares to "manually-verified values". Not household golden cases. Hub data CC BY 4.0.
- CMS "MAGI in the Cloud" official CMS build (registry2.omb.gov Docker image per ene-testing/mitc/README.md) — not public.
- OpenFisca US, Nava, MITRE, Atlas: no public SNAP/Medicaid test-case sets found in this pass.
- Synthea: synthetic health records (clinical), no income/household eligibility data. Not relevant except for person demographics.
- FNS SNAP eligibility system go-live requirements and APD testing FAQs (https://www.fna.usda.gov/sso/snap-eligibility-system-golive-requirements):
  define UAT/pilot criteria, no cases. Relevant to certification process, not to case content.
- State UAT scripts (Arkansas, Iowa, Kentucky, Washington procurements): attachments mention UAT; no published scripts with expected results found.
- CBPP "A Quick Guide to SNAP Eligibility and Benefits": worked family-of-3 example; CBPP copyright -> re-derive.

## Coverage gaps (no good published golden cases found)

- SNAP expedited service determination and 7-day timeliness (only QC flag EXPEDSER and prose criteria).
- ABAWD with time-limit counting across months and H.R.1 exemptions: only PolicyEngine unit tests (no month-by-month clock cases).
- Notices (content and correctness): only Colorado renewal workbook narrative examples.
- Renewals / ex parte: 2 SHVS scenarios + Colorado workbook examples; no SNAP recertification cases.
- Integrated Medicaid+SNAP same-household cases (combo case) with both outcomes: none found.
- Colorado options: CO SNAP SUA tiers, CO BBCE limits, CO MSP/Buy-In, CO non-MAGI (HCBS, LTC; verify whether CO runs a medically needy program), CO-specific
  aid codes and hierarchy (MA Aid Code Hierarchy desk aid exists as a rule source, not cases).
- Account transfer (FFM <-> state) payload tests: CMS sample payloads exist (3), Colorado is SBM (Connect for Health Colorado) so less relevant.
- Non-MAGI with resources, spend-down, transfer-of-assets penalties: PolicyEngine LTC tests only (unit level).
