# Notes on unread sources: FNS HB901 v2.5 ch1, 4, 5, 7, 9 + appendices; CMS SHO #25-003

Prepared 2026-11-11. Sources treated as untrusted data; nothing executed.

- HB901: [FNS Handbook 901 v2.5](https://www.usda.gov/sites/default/files/guidance-documents/fns-handbook901-version2.5.pdf). Citations give the HB901 section number; `L####` refers to a line in a private Markdown extraction of the PDF and is kept only as a rough locator.
- SHO #25-003: [CMS State Health Official letter #25-003](https://www.medicaid.gov/federal-policy-guidance/downloads/sho25003.pdf), extracted with `pdftotext -layout`. Citations give the letter page.

Note on HB901's legal weight (every page footer): "Guidance documents lack the force and effect of law, unless expressly authorized by statute or incorporated into a contract."

> **Editor's note (reviewed 2026-11-11).** Two conclusions in these notes were checked against the source text and **rejected**:
>
> 1. *"One combined APD" is not supported* — rejected. HB 901 §3 says: "When a project involves multiple federal partners, one combined APD is developed. The State agency is required to submit the APD separately to each agency that is providing FFP." Each agency still approves under its own rules.
> 2. *"HB901 does not say a contractor may not perform UAT"* — rejected. HB 901 §6.7.2 says: "The contractor development and implementation team must not perform UAT testing." The A15 staffing table cited below is an *example* that lists the contractor among test leads, while testers are state staff. The proposal keeps the §6.7.2 wording.
>
> The point about SNAP merit-system staff for client-contact work during the pilot (§5.2.4) stands and is worth confirming with FNA.


---

## CMS SHO #25-003 (August 6, 2025)

Title: "Streamlining Medicaid Enterprise Systems (MES) Templates to Improve Monitoring and Oversight to Ensure Fiscal Integrity." Signed by Caprice Knapp, Acting Deputy Administrator and Director.

### What it changes (p.1)
> "This letter documents CMS' ongoing efforts to reduce state burden and streamline and standardize state project reporting and oversight in the following areas: o MES Advance Planning Documents (APDs) and MES Medicaid Detailed Budget Tables (MDBT) templates o Operational Reporting Requirements o Analysis of Alternatives (AoA) o Submission of Project Status Reports o Request for Proposal (RFP) Checklists o Sunsetting the Electronic Visit Verification (EVV) Outcomes-Based Certification (OBC) to align with Streamlined Modular Certification (SMC)"

### Effective date (p.2)
> "States should fully transition to the new templates across the MES lifecycle. We expect states to transition to the new templates within 6 months of the Paperwork Reduction Act (PRA) approval."
Templates are under OMB control number 0938-1268 (CMS-10536) (footnotes 4, 6). The letter gives no calendar date for PRA approval. Check medicaid.gov / reginfo.gov for the CMS-10536 approval date to compute the deadline.

### Background: SMC is metrics-based (p.2)
> "In April 2022, State Medicaid Director Letter (SMDL) 22-001 announced the transition to the SMC framework, which emphasizes metric data and operational reporting rather than checklists."
> "These templates are expected to expedite the review process for funding, encourage states to consider alternatives and reuse, standardize operational and status reporting to ensure the project is progressing according to the milestones in the APD, and facilitate a unified certification process applicable to all MES modules."

### APD templates (p.2-3)
> "CMS is introducing three APD templates to improve standardization of submissions: the MES APD template, the MES Operational APD (OAPD) Template, and the MES MDBT+CHIP template."
> "states should use the MES APD template for all APD submission types (Planning, Implementation, Update, and As-Needed) except Operational. The MES APD template is tailorable to a state's needs and may be used to request individual Medicaid Management Information System (MMIS) or Eligibility and Enrollment (E&E) project funding. The MES APD template can also be used to request funding for combined MMIS and E&E projects. These APD templates will replace the current OMB-approved template for E&E APDs."
> "states should complete and submit the new OAPD template to obtain CMS approval for APDs requesting funding for maintenance and operations (M&O) or Operational Advance Planning Document (OAPD) Update submissions, whether for MMIS, E&E, or both."
> "States can now combine MMIS and E&E submissions" [MDBT+CHIP template] (p.3)

"Combined" here means MMIS + E&E within CMS. It says nothing about a joint CMS + FNS APD.

### Operational reporting (p.3-4) — the ORW
> "States' MES solutions must produce data, reports, and performance information that would contribute to program evaluation and continuous improvement in business operations as a condition of enhanced Medicaid federal matching for MES expenditures (42 CFR 433.112(b)(15) and 433.116(b), (c), and (i)). Each state seeking enhanced Medicaid federal financial participation (FFP) should include operational system data with its OAPD submissions." (p.3)
> "CMS views the metrics included in operational reports as indicators measuring whether associated systems and modules meet CMS-required and/or state-specific outcomes ... CMS can request that states update metric definitions and resubmit the modified metrics via an APD. States that do not submit operational reporting will be considered non-compliant with the applicable regulations and could lose enhanced Medicaid FFP or CHIP federal funding." (p.3)
> "The updated Operational Report Workbook addresses these concerns by standardizing data submission formats and allowing states to update the viability and value of their metrics." (p.3)
> "States will submit monthly operational reports using the Operational Report Workbook and upload the file to the appropriate metrics file location in the CMS designated repository. Additionally, every OAPD submission should include an attestation specifying the CMS repository folder location of the submitted Operational Report Workbooks. ... Reports should cover data from the system's go-live date or the last OAPD submission through the most recent month of available data. ... CMS recommends one module per Operational Report Workbook." (p.4)
> "The enhanced insight into state system performance and related business operations facilitated by improved state operational reporting should better allow states to demonstrate their ongoing compliance with applicable federal regulations, and help mitigate fraud, waste, and abuse" (p.4)
Footnote 7 (p.4): "In accordance with 45 CFR § 95.615, the state must allow the Department of Health and Human Services (DHHS) access to the system in all of its aspects, including operational records, at such intervals as are deemed necessary by the Department to determine whether the conditions for approval are being met".

Also updates the "MES Data Submissions and Intake Procedures Manual" (p.3-4).

### Analysis of Alternatives (p.4-5)
> "states must conduct and document an AoA per 45 CFR 95.610(b)(3), and are expected to include an associated enterprise reuse plan to help ensure compliance with 42 CFR 433.112(b)(13)." (p.4)
> "States will be expected to use the template to complete Section 5 of the new MES APD and/or Appendix A of the new MES OAPD." (p.4)
> "The market research portion of the AoA requests that the state collaborate with other states on systems available for reuse." (p.4)
Relevance: reuse is now a formal AoA step. An openly licensed toolkit is something another state's AoA could find and score. A noncommercial license may make reuse harder (vendors who build for states are commercial actors).

### Monthly project status reports (p.5)
> "States submit monthly project status reports in support of MES projects receiving enhanced Medicaid FFP, as noted in the Streamlined Modular Certification (SMC) for MES Guidance ... States will use the new Project Status Report template to provide consistent, structured data for reporting and enable timely decision-making and adjustments to project plans. This template provides the state with a vehicle for submitting timely updates on the project's status to the CMS MES State Officer, including progress since the last report, funding status, risks, issues, and achievement of major milestones. States pursuing certification will submit a project status report monthly. States will submit the project status report using the project status template and upload the file to its appropriate file location in the CMS designated repository."

### RFP checklist (p.5)
> "Following OMB PRA approval, states should include a completed RFP checklist with all RFPs submitted to CMS for prior approval, consistent with 45 CFR 95.611."

### EVV moves into SMC; SMC Intake Form (p.5-6)
> "All modules, including MMIS, E&E, and EVV, will be input into the SMC Intake Form." (p.6)
> "States should provide evidence for both outcomes and the Medicaid Conditions for Enhanced Funding (CEF) for all modules" (p.6)
> "EVV modules will now be adjudicated with the measures of 'Evidence Satisfactory' and 'Evidence Not Satisfactory.' States will continue to receive observations and recommendations from CMS following the completion of an Operational Readiness Review and Certification Review." (p.6)
> "States will submit to CMS all germane SMC artifacts and evidence, including privacy and security documentation. ... Failure to provide the pertinent SMC artifacts and evidence may cause delay or disapproval of certification." (p.6)
> "To request a certification review, a state's system should have been in production for at least six months and have data from the certification request date to the most recent month-end." (p.6, under EVV bullet "Metrics and Operational Reporting for Certification")
> "The cadence of reporting addresses the timing of report submission to CMS, which will remain quarterly for EVV modules, while the frequency refers to the capture of the metric data within the Operational Report Workbook, which will remain monthly. For all other modules, states should adhere to operational reporting guidance specified in this SHO." (p.6)
Footnote 10: the MES Certification Repository is `https://cmsgov.github.io/CMCS-DSG-DSS-Certification/` (a GitHub Pages site).

### Governance (p.2, p.7)
> "Early and ongoing collaboration between program and IT teams helps break down organizational silos, improves project oversight" (p.2)
> "CMS strongly encourages state Medicaid and CHIP program officials to involve their Medicaid and CHIP CIOs, or, where applicable, their State CIOs, as stakeholders in all Medicaid and CHIP IT projects." (p.7)

### What SHO 25-003 does NOT do
- No mention of SNAP, FNS, or a joint federal APD.
- No mention of agile, continuous integration, automated evidence, or machine-readable submission formats beyond "standardizing data submission formats".
- No new security requirement; only "privacy and security documentation" as SMC artifacts.
- No calendar effective date (keyed to PRA approval + 6 months).

---

## HB901 Chapter 1 — Getting Started (L1230-2508)

### Joint projects: separate APDs to each agency
> "The DHHS also has an APD process. Consequently, in joint projects, State agencies must submit APDs to all federal agencies from which they are requesting FFP and/or grant funding for an IS project." (1.1, L1398-1399)
> "The FNS HB901 provides guidance for USDA APD processes ONLY. It does not provide guidance for APD requirements for other federal agencies that may also be providing Federal financial participation." (1.1, L1362-1364)
> "These joint systems are often completely integrated, and the process of oversight has to be coordinated between FNS and DHHS. Each federal agency is responsible for review and approval of its own costs and federal funding participation in State IS projects." (1.9.4.1, L2297-2299)
Reading: a state submits to every agency; each agency approves its own share. HB901 does not forbid one document sent to both, but each agency reviews it under its own rules. Do not claim "one combined APD approved jointly".

### Thresholds
SNAP PAPD and IAPD: "For all projects ≥$6 million total project costs" (Tables 1-2, L1596, L1629). Submit "at least 60 days before project initiation"; FNS "Reviews within 60 days".
> "State agencies should assume that incremental efforts which may be under approval thresholds individually, but which support a unified outcome, will be regarded by FNS as a single project, and that a cumulative threshold will apply." (1.5.1.1, L1609-1611)
Relevance for agile: splitting work into small increments does not avoid APD thresholds.

### M&O: no annual APDU, but enhancements need prior approval
> "FNS does not require annual APD Updates to approve the funding of maintenance and operations activities. ... However, prior approval of an APD is required for M&O when significant platform changes or software enhancements are made to the system." (1.5.1.3, L1638-1642)
> "Even if the planned changes do not meet these criteria, the State agency should keep FNS informed during the M&O phase." (L1665)
Footnote ‡ (L1671-1672): "Even purchases which do not require approval in an APD must be procured through free and open competition. Request for Proposals (RFPs) and contracts are subject to FNS approval."
Contrast with CMS: CMS requires OAPDs with monthly ORW data for M&O funding. FNS does not require annual APDUs for M&O.

### Implementation phase includes UAT, pilot, rollout
> "The implementation phase activities include the SDLC activities for development, testing and implementing the system, to include user acceptance testing, pilot testing the system, and accomplishing full roll-out. All of these SDLC activities are monitored for how closely they follow the activities described in the approved IAPD." (1.7.2, L1934-1937)
Figure 9 (L1880-1897) implementation sequence ends: "Generate status reports, annual APDU, and APDU As-Needed / FNS Post Implementation Review / IAPD Closure".

### APD closure
> "When planning or implementation activities are completed, the State agency must submit a final APDU. USDA will confirm all activities are complete as described in the approved APD ... Once confirmed, FNS and the State agency may close the APD. This step is necessary to officially end all approved activities, document actual costs incurred, and terminate federal funding activities." (1.7.3, L1942-1946)

### FNS role during testing, pilot, rollout, PIR
> "Arranging visits to State agencies during the project life cycle, especially during testing, pilot, and roll out, as appropriate" (1.8.1, L2019-2020)
> "Arranging dates and preliminary agenda for post-implementation reviews and preparing final reports, including any corrective action requirements, as necessary" (1.8.1, L2022-2023)
> "Providing technical assistance (e.g., training, acceptance testing, budgeting, and cost allocation)" (L2025)

### State responsibilities
> "Demonstrating through thorough testing that the system meets all program functional and performance requirements" (1.8.2, L2119-2120)
> "Enforcing contract provisions; including boilerplate requirements, key personnel clauses, programspecific requirements, and performance guarantees" (L2133)
> "Adhering to federal requirements for status reports, State plans, funding process requirements, and policy implementation" (L2135)

### Roles
> "Project Director—... A project sponsor may serve as a project director but not as a project manager." (1.9.1, L2238-2240)
> "Project Manager—... responsible for reviewing deliverables for accuracy, approving deliverables, and providing status reports to management." (L2242-2244)
> "Project Team—Team members (State program, FM and IT staff; and their contractors)" (L2246)

---

## HB901 Chapter 7 — Project Management (L13985-15159)

### Testing, pilot, rollout guidance (adds to ch6)
> "Make extensive testing a priority (e.g., performance, usability, acceptance, and regression testing) • Use the system pilot to discover problems that could become disastrous during rollout and beyond • Provide documentation of the pilot evaluation to FNS • Complete testing before starting a rollout • Plan a reasonable rollout schedule to provide the opportunity for making course corrections and adjustments along the way o Use a phased approach o Avoid a 'big bang' approach" (7.1.1, L14155-14170)
> Recurring APD risk: "Not performing adequate testing (including the pilot) before and after implementation of a new system or major enhancement(s)" (7.4.3.2, L14762-14763)
> "Placing a large focus on front-end/user interface modules while neglecting other critical elements of the system such as security, system capacity, notices, and reporting" (7.4.3.3, L14784-14785)

### Contractor control risks
> "Over reliance on the contractor to prepare required APD documentation, which can render a State vulnerable to the contractors' idea of what would be best, leading to costly consequences" (7.4.3.2, L14734-14735)
> "Giving the contractor too much control, responsibility, or authority, or both on behalf of the State agency (i.e., abdicating strategic decision making and fiscal responsibilities)" (7.4.3.3, L14776-14777)
Relevance: a toolkit built and run by the vendor that also produces the evidence needs state ownership of the go/no-go judgment.

### Change control / retroactive approval
> "Not realizing that changes in cost, scope, and schedule, or procurement changes, must be submitted as an APD Update (APDU) and approved by FNS before new significant costs may be incurred (i.e., erroneously thinking retroactive approval can be sought)" (7.4.3.3, L14795-14797)
> "Incremental or limited funding" listed as a common APD project risk (7.4.3.1, L14703)
> Project Management Plan: "Any changes to the Project Management Plan must be approved by the Change Control Board (CCB)" and baselines "can only be updated through the formal change control process" (7.4, L14460-14494). Includes a "Configuration Management Plan" that should "record and report the implementation status of the changes, and support auditing to verify conformance to requirements" (L14471-14473).

### RTM
> "An RTM tracks requirements from origination to implementation in the final result. It supports testing activities by linking requirements to specific tests for requirements. ... after project completion it provides a history of the system from inception to decommissioning." (7.4.1, L14528-14533)
Relevance: the evidence ledger is an RTM with automated links. Good framing.

### Risk management continues in M&O
Table 39 (L14830): M&O — "Risk management activities are performed for periodic system reauthorization (or reaccreditation) or whatever major changes are made to the IT system in its operational, production environment".
> "Risk management should be reported as part of project status reports." (7.4.3, L14662-14663)

### Monitoring: QA independence
> "Quality Assurance (QA) is a key activity of monitoring and control. It may be performed by a QA contractor or by qualified State agency staff. The QA contractor must not be the same as the project management contractor. Likewise, the State QA staff should be independent from the project management or development staff." (7.5.1, L14862-14864)
> "FNS expects State agencies to establish a plan for monitoring the development of State automation projects as a condition of project approval. Overall project monitoring includes specifically monitoring project procurements and formal acceptance of contracted services." (L14845-14847)
Relevance: the toolkit should not be positioned as QA run by the build vendor. Independent QA/IV&V must be separate.

### Status reports to FNS
> "They should submit status reports to FNS to ensure overall program administration. FNS may require the State agency to provide contractor and project status reports for informational purposes throughout the project. These may be outlined as conditions for funding approval." (7.5.1, L14870-14873)
> "The results of State agency monitoring may be reported in routine status reports in addition to APDUs." (L14875)
> "In some cases, contractor reports can be forwarded directly to FNS with no additional work. ... Status reports need not be lengthy to be informative and meet FNS expectations. Thorough status reports make annual APDUs easier to compile." (L14883-14886)
Content list (L14889-14935): period covered; narrative status; activities incl. "Explain if activities were added or omitted from those in the approved APD"; accomplishments; "Major deliverables received/approved"; areas behind schedule; status of old and new problems; "Status of any items in the State's risk assessment"; staffing changes; budget variance with "Previous quarters should show actual costs / Future quarters should show budgeted costs"; "Contractor bills and payments made".
Note: no fixed frequency is set in ch7 (contrast CMS: monthly). Quarterly budget columns imply a quarterly view.

### FNS monitoring and System Functional Requirements Review
> "FNS reserves the right to conduct on-site monitoring through project status visits; local or state agency reviews, or both; participating in user training; and participating in User Acceptance Testing (UAT)." (7.5.2, L14941-14943)
> "FNS may elect to conduct a System Functional Requirements Review after the system has passed UAT, before the pilot, or before the deployment of software. FNS may decide to do all of these. Please note that this does not have to be an on-site review. The review may be conducted by reviewing UAT or Pilot Evaluation documentation, or both, provided by the State agency." (L14950-14953)
Reasons include "Verifying that UAT was thorough and successfully completed", "Ensuring that all policy to be administered through the system is accurate", "Analyzing the integrity of data capture, edits, and calculations", "Ensuring the system interfaces successfully with other program IS and external entities, including EBT" (L14957-14971).
Relevance: a desk review from UAT/pilot evidence is explicitly allowed. The evidence ledger can feed this directly.

### Post-implementation review (PIR)
> "Project closure may include a post-implementation review, preferably six months after implementation and rollout are completed. The purpose of conducting a post-implementation review is to gather the information required to meet IAPD process responsibilities. The review may be conducted by the State agency as a deliverable, by FNS, or a combination." (7.6, L15023-15025)
> "The post-implementation report may be used for an internal State agency review of the project's closure or in response to an additional requirement imposed by FNS prior to the closure of the project's APD." (L15026-15028)
> Report covers "an assessment on the effectiveness of project management, risk management, communications, change management, issues management, implementation and transition, and performance of the project team" plus "key project metrics" (L15054-15057). "The PM must present or distribute the post-implementation report to members of the responsible organization and should share it with FNS." (L15057-15058)
> "A critical reason for the post-implementation review is to ensure that the system is reviewed and evaluated before the warranty period expires." (L15062-15063)
Note: PIR is "may", one-time, about project management. It is not ongoing operational metric reporting.

### Other
> "State agencies may choose to have FNS participate as 'ex-officio' members of a project's executive steering committee." (7.3, L14403)
> PM "Does no work other than managing the project" (L14210); "Assigning a full-time, experienced, formally trained, certified professional Project Manager (PM)" (L14110).

---

## HB901 Chapter 4 — Procurement (L6537-9580)

### Thresholds for FNS prior approval (SNAP)
Table 16 (competitive, L7240-7256): SNAP RFP and contract — "Total cost of the individual procurement is ≥$6M"; SNAP contract amendment — "For any amendment ≥ 20% of base contract cost (cumulative)". FNS "reviews within 60 days".
Table 17 (non-competitive, L7258-7277): SNAP SOW/PWS + Sole Source Exception Request and contract — "For all procurements with total cost ≥ $1M".
> "Prior written approval from FNS is required for SNAP MIS and SNAP EBT contract amendments that cumulatively exceed 20 percent of the base contract costs. ... The base contract includes only the base period and does not include any options or amendments." (4.2.4.3, L7104-7106)
> "All SNAP contract amendments, regardless of cost, must be sent to FNS for recordkeeping purposes." (L7089-7090)
> "a competitive procurement may transition to a noncompetitive procurement status if the procurement exceeds its available base period, or its options" (4.3.1, L7234-7237)
> "All RFPs, contracts, and their subsequent amendments that exceed applicable thresholds must be submitted to FNS for review and approval before their release or execution. If a State agency proceeds without FNS approval, it may be held liable for any incurred expenditures." (4.3.2, L7281-7283)
> SNAP provisional approval: "This occurs when FNS has not provided written approval, disapproval, or a request for additional information within 60 days of acknowledging receipt of the submission." (L7405-7407)
> "The RFP should be available for vendor review and response for at least 90 days." (4.2.2.3, L6879) and "FNS requires that all solicitations remain open for a minimum of 90 days" (4.9.3.2, L9405-9406).

### Separate submissions to each federal agency
> "The State agency is responsible for submitting the RFP, contracts, and their subsequent amendments to each individual federal agency that may be participating in the federal funding of the project. In other words, separate copies must be submitted to FNS and Department of Health and Human Services (DHHS) agencies if both are contributing FFP to the project." (4.3.2, L7283-7286)

### What FNS recommends the RFP require of the contractor (testing, deliverables, incremental demos)
> "FNS recommends that the RFP require the contractor(s) to perform the following activities: • Use configuration management (CM) software during design, development, and testing • Develop requirements documents (which may include use cases) that require sign-offs when accepted by the State agency • Implement a change control process to document all requested changes to the system and to track their status ... • Conduct an incremental system demonstration every few months during development, as appropriate • Provide detailed system and functional requirements, system design specifications, source code with inline comments, and a complete system installation guide • Ensure that the system under development occurs in accordance with FNS program requirements and regulations" (4.6.1, L7525-7543)
> "The State agency should consider several other performance requirements ... These include the impact of plans on project timelines and schedules for data migration, testing and pilot activities, and transitioning any incumbent contractors." (L7545-7548)
> "Ensuring that RFPs contain enough detail to clearly define requirements and the process by which detailed requirements may be added later, depending upon the development methodology being used" (4.9.1, L9218-9220) — a nod to iterative requirements.

### State acceptance before payment
> "The RFP and the resulting contract should stipulate that payment will occur following review and acceptance of each major deliverable by the State agency. Major deliverables may include the detailed system design, as well as system and functional requirements documents." (4.7.8, L8296)
> "Prescribed Payment Terms—Payments or holdbacks are prorated according to the relative value of, and tied to acceptance of, deliverables. In many cases, this includes a final payment that is a substantial percentage of the total contract value (e.g., 20 percent). This amount is not paid until the system is accepted or certified." (4.7.2, L8002-8005)
> Table 20 standard provisions include "System acceptance criteria", "System warranty provisions", "QA provision", "Reporting requirements", "Access to facilities and records" (L8134-8135).
> SOW should list "Contract Deliverables—... This should also include acceptable performance criteria or measurements for each deliverable." and "Management Plan – Identifies ... the type and frequency of project status reports, and the review and approval process for work performed." (L9376-9389)
> "When you need the contractor to perform a task, you must use the word 'SHALL' for that tasking to be legally binding." (L9291-9293)

### QASP (state surveillance of the contractor)
> "The QASP details how, when, and by whom the State agency will survey, observe, test, sample, evaluate, and document contractor performance results to determine whether the contractor has met the required standards for each objective in the PWS. The QASP is intended to be a 'living' document" (4.7.4, L8098-8101)
> "The QASP is not required by FNS for RFPs and contracts. However, it is recommended as a best practice" (L8106-8107)
Relevance: the toolkit's rules + evidence ledger can be framed as the machine-readable part of a QASP. Good hook, and it keeps the state as the surveillance owner.

### Software escrow
Only mention (4.7.2, L8027-8034): "Most contractors are willing and expect to abide by a combination of holdbacks (i.e., payment percentage terms), liquidated damages, and software escrow." Footnote: "Software escrow is the deposit of the source code of software with a third party escrow agent. Escrow is typically requested by a party licensing software (the licensee)". No escrow requirement. Escrow is a licensee tool; under HB901's model the state owns custom code, so escrow is relevant only to vendor-owned or pre-existing components.

### Ownership, federal license, IP (FNS equivalent of CMS CEF05/CEF06)
> "There are several policy requirements that State or local governments must include in all RFPs and contracts for any software or software modifications and associated documentation that is designed, developed, or installed with FFP. These include ownership rights and a broad federal License, among others, as provided in 7 CFR 277.18(l)." (4.7.7.6, L8248-8251)
> "Proprietary vendor software packages and operating systems (OS) that are provided at established catalog or market prices and sold or leased to the public are not subject to these licensing and ownership provisions." (4.7.7.7, L8265-8267)
> Table 20 lists "Ownership, Licensing and Intellectual Property Rights": "Federal Ownership License (7 CFR 277.18(l)(1)(ii)) o Copyright licensing ... o State agency ownership of intellectual property (7 CFR 277.18(l)(1)(i))" and FNS-required provision "FNS has royalty-free rights to use software and documentation developed" (L8146-8147).
> 4.10 summary: "The RFP and contract must include ownership rights and a broad federal License as provided in 7 CFR 277.18(l)" (L9476-9477).
> Contract Clauses: "Because the acquisition of rights to computer software and computer software documentation is a special interest for use of FFP, Contract Clause language should include relevant clauses for acquiring ownership rights for software being procured using FFP." (L9391-9393)
> Access: "The State agency must make procurement records available to FNS and provide access to all aspects of the IS project. This includes design, development, operation, and work performed by any source ... Failure to provide this access ... will result in suspension or termination of FFP" (4.7.7.5, L8234-8241)

### Conflict of interest — who may test/evaluate
> "The same contractor must never: • Define the work and then bid on it, or • Perform the work and then evaluate it." (4.8.6, Figure 40, L9128-9134)
> Table 22: "Development | Quality Assurance | Yes | ... The contractor cannot provide objective QA of its own work." and "Quality Assurance (or any other function) | Independent Verification & Validation | Yes | IV&V is a review process performed by an organizational entity that is independent of the QA contractor or any other project role." (L9180, L9191)
> Contractors enter a conflict when asked to "Review products or deliverables they have helped develop" and "Define performance parameters during planning against which they will be evaluated, or measure their own performance as implementers" (L9152, L9168-9169).
> M&O: "the State agency should provide for QA or Independent Verification and Validation (IV&V) services for system enhancements. These types of contracts must be with a separate contractor than the M&O contractor" (4.8.5.5, L9073-9075).
> DDI contractor duties include "Testing and demonstrating system functionality or enhancements" and "Developing test plans and scenarios for users of system enhancements" (4.8.5.4, L9032-9034).
Reading for the toolkit: the DDI vendor may run its own tests and produce evidence (that is QC). But if the DDI vendor authors the rules catalog thresholds or runs the go/no-go dashboard, it is "measur[ing] their own performance as implementers." The state, QA, or IV&V must own the rules and the pass/fail judgment. Also, if the toolkit's owner is a different contractor (QA/IV&V), it cannot also build.
Note: ch4 does not say a contractor may not perform UAT. It does require separation of building from evaluating. UAT by state users is the clean model (ch6 already covers that).

### State keeps decision authority
> PM contractor: "the State agency remains responsible for project management and federal reporting. ... The State agency must retain all decision-making authority and accountability for project management. The State agency's project manager or project director is responsible for all communications with the federal funding authorities." (4.8.5.2, L8942-8947)
> PM contractor duties include "Ensuring that testing and training are conducted properly and meet State and federal requirements" and "Producing periodic status reports for State decision makers, FNS, and other stakeholders" (L8961, L8980).

### Contract type
> "Circumstances rarely arise when FNS would support use of a cost-reimbursement contract for a system project. Therefore, HB901 focuses on fixed-price RFPs and contracts." (4.8.1, L8426)
> FFP fits when "Requirements are stable" and "Processes or methods are mature" (L8459-8463).
> T&M "may be used when it is not possible to accurately estimate the extent or duration of the work" but "provides no incentive to the contractor for controlling costs" (L8482-8486). 7 CFR 277.14 standard: "Use time and material-type contracts only after determining that no other contract is suitable and that the contract includes a ceiling price" (L7453-7454).
Relevance for agile: HB901 leans to firm fixed price per deliverable. Agile vendors often use T&M/capacity. The proposal should tie payment to accepted increments with evidence (fits "incremental payment points based on the schedule by deliverable and/or phase", L8006-8007).

### Contract length
> "FNS recommends that the contract length be limited to 5 to 10 years, inclusive of option years." (4.8.4, L8813)

### Free software offers (relevant to toolkit licensing) — see also A16.8
No ch4 text on open source. Appendix A16 covers it (below).

### SNAP EBT timing table (Table 19, L7738-7805) — relevant UAT/Go items
"Federal Acceptance Test Plan | -4 to –2 months | Requires FNS approval when converting to a new processor"; "User Acceptance Test | -2 months | FNS concurrence required for a 'GO' decision". This is EBT processor conversion, not E&E. But it shows FNS concurrence on GO.

---

## HB901 Chapter 5 — System Planning (L9581-11736)

### SIRT: when FNS uses it (adds to ch6)
> "FNS has developed a SNAP System Integrity Review Tool to be completed by State staff for review by FNS Regional Office staff, to ensure automation projects adhere to all policy requirements." (5.3.1.4, L10397-10399)
> "The SNAP APD process described at 7 CFR 277.18 states that FNS may conduct reviews of the system either prior to pilot, once it is fully operational statewide, or both. The review may include regulatory and policy requirements, system controls and performance, and system security, amoung other topics, as its foundation. Although the System Integrity Review Tool is intended to be used prior to User Acceptance Testing, and again after statewide implementation to validate functionality, it is also useful during requirements analysis. ... FNS will use this same tool for UAT, pilot, and possibly post-implementation reviews." (L10401-10407; endnote 40 cites 7 CFR 277.18(g)(2)(i)-(iii) "Basis for continued Federal financial participation")
> "If a requirement is not testable, or a required regulatory capability is not part of the design, testing will fail to accomplish its purpose." (L10392-10394)
Policy-related system requirements to consult: "SNAP – Requirements in 7 CFR 272.10(b)(1), (b)(2)(vii) through (xiii), and (b)(3)" and "SNAP – System Integrity Review Tool" (L10317-10319).
Relevance: SIRT is used at four points (requirements, before UAT, pilot, after statewide). A continuously evaluated SIRT mapping supports all four. The post-statewide SIRT review is the closest FNS thing to post-rollout oversight, and it is a point-in-time review, not periodic reporting.

### Contractor staff and client contact; waivers
> "State agencies should keep in mind that tasks involving client contact are restricted to State merit system personnel unless FNS approves use of non-merit or vendor staff to perform certain tasks." (5.2.4, L10135-10137)
> "Where technology is used to supplant or supplement the duties of merit staff, or where communication with applicants or participants changes the way applications are processed, changes are reported, or notices to participants are delivered, States should notify their FNS regional offices to ensure that the new processes are in compliance with SNAP policy or identify what waiver requests might be necessary." (L10129-10133)
Relevance to assumption "a contractor may not perform UAT or the pilot": HB901 does not say that. The real limit is SNAP merit-system rules for client-facing eligibility work. A pilot that processes real SNAP cases needs merit staff (or FNS approval). Testing by contractors in non-production is not barred.

### Agile / methodology
> "The technical approach should consider which system development methodology it prefers or uses as a State agency standard (e.g., waterfall, iterative, spiral, agile, etc.). This decision might be based on vendor proposals" (5.4.3, L11014-11017)
> "if the State agency determines through its feasibility study that an Agile approach is the preferred development methodology, and that they want a COTS-based solution, these should be stated in the RFP." (L11028-11030)
> "Is an Agile approach to an enhancement compatible with the waterfall methodology being used to manage the systems lifecycle?" (L11038-11039)
> "Open Systems Architecture IS NOT the same as Agile development. OSA is a design principle and is compatible with all development methodologies" (5.5.2.1, L11319-11321)
> OSA "supports: • Design for affordable change • Employment of evolutionary development" (L11331-11333)
HB901 is methodology-neutral. It accepts agile but gives no agile-specific oversight model (ch2 2.2.4.2 and ch6 have more; not re-read here).

### Data conversion
> "The final test plan must include test cases and scripts demonstrating that data migration was accomplished successfully." (5.4.1, L10856-10857)
> Planning questions include "Is there a concurrent period of operation where data will be maintained in both the source system and the target system? ... Which system contains the official record during concurrent operations?" (L10912-10917)
> "During verification, there may be a need for a parallel run of both systems to identify areas of disparity and forestall erroneous data loss. Verification through parallel processing does not occur during pilot testing, but does occur in earlier project phases." (L10941-10943)
Relevance to "pilot must be live with the new system as system of record": ch5 implies parallel runs are a pre-pilot activity and the pilot is not a parallel run. It does not state "system of record" in those words. Ch6 (already read) is the main source.

### Transferability / reuse (supports openness)
> "A major objective of FNS' financial stewardship responsibility is to assure that Federal and State Governments do not pay repeatedly for the re-development of desirable systems already implemented with public funds." (5.5.1, L11069-11071)
> "FNS expects that all State agencies will help maximize limited funding by supporting system transfers and/or reuse and providing assistance to help others achieve success." (5.5.1.2, L11159-11160)
> Recommended transfer/reuse package includes "Source code", "Transfer Package Testing o test procedures for transfer o test cases/scenarios/scripts for transfer" (L11199, L11245-11249). "The State agency should include a specific task and deliverable requiring its contractor to prepare a transfer/reuse package" and keep it updated during M&O (L11276-11279).
> "If only the incumbent contractor has the expertise to facilitate a transfer, due to accessibility of the code or other materiel, the State should seriously question the selection of that system for transfer." (L11296-11298)
> "FNS will not accept the results of an alternatives analysis which compares only a pre-selected favorite to clearly non-viable 'straw man' options." (5.3.2.1, L10518-10519)
> CBA: "it does not require calculating a number of years to the break-even point or tracking and reporting the CBA beyond initial approval of the IAPD." (5.3.3, L10775-10776) — FNS does not track benefits after approval.
Relevance: test cases and scripts are part of the transfer package. The rules catalog and test evidence could be packaged as reuse material. A noncommercial license on a toolkit embedded in a federally funded system works against the transfer goal.

### Cloud/SaaS
> "SaaS shares many characteristics of traditional COTS software applications, including intellectual property rights." (L11631-11632) Commercial COTS/SaaS at market price is outside the 277.18(l) ownership rule (see 4.7.7.7).

---

## HB901 Chapter 9 — Systems Security (L16718-18790)

### Scope: development and test environments too
> "State agencies are required to secure information and EBT systems involved in the administration of FNS programs. ... State agencies are responsible for implementing and maintaining a program to ensure adequate security is provided for personnel, information collected, processed, transmitted, stored, or disseminated into general support systems and major applications. This includes the security of all projects being developed, implemented, and tested, as well as operational systems." (9.1, L16823-16830; cites 7 CFR 277.18(m))
> "When security programs are part of an IS implementation, Federal financial participation (FFP) may be used to implement security for the information systems." (L16830-16831)

### Standard: state choice, FISMA/NIST recommended (not mandated)
> State IS security plan goal: "Determine appropriate IS security requirements using either recognized industry standards or compliant with federal standards governing security of federal IS and information processing" (L16835-16836)
> "FISMA is recommended as a best practice for State agencies using FFP to administer federal programs." (9.1.1, L16915)
> "State agencies should develop IS security programs based on federal standards outlined in FISMA, OMB Circular 130, and NIST Guidelines." (L16952-16953)
Table 45 lists NIST SP 800-18, 800-30, 800-34, 800-35, 800-53 rev5, 800-61, 800-160, 800-70, 800-88, 800-115, 800-124, DISA STIGs.
Contrast: CMS requires MARS-E/ARC-AMPE-based SSP, SAR, POA&M for E&E. FNS has no SAR or POA&M template in HB901. "POA&M" in the security sense does not appear; the nearest is "an action plan with scheduled dates of milestones" (9.7).

### The only recurring post-rollout FNS obligation found: biennial security review
> "State agencies must review the security of IS on a biennial basis. This includes physical and data security, operating procedures, and personnel practices. – 7 CFR 277.18(m)(3)" (L16956-16957)
> "State agencies are responsible for conducting the security review of systems that administer FNS programs at least biennially. State agencies must provide a written summary of their findings and determination of compliance with requirements to FNS upon request or at least biennially after completion of the Information System Security Review. The State agency includes an action plan with scheduled dates of milestones which, when completed, will correct any security weaknesses." (9.7, L18627-18633)
> Security plan objectives include "Measure progress in achieving targeted goals • Provide FNS with an IS security status report" (9.7.1, L18673-18675)
> Security plan appendices list, per sensitive application: "Date of last system evaluation o Date of last system certification or recertification o Date of next evaluation or recertification • Summary of the risk analysis reports" (Table 52, L18684)
Relevance: a dashboard that tracks security findings and their milestone dates directly produces FNS's biennial "written summary" and "action plan". Cadence is biennial, not monthly.

### Continuous risk assessment; change-triggered review
> "Key risk analysis activities are conducted when a system is first implemented and whenever significant modifications are made to the system. However, because threats are always evolving and never abate, risk assessment must be a continuous process." (9.2.2.1, L17164-17166)
> "Risk management for an IS security program is a continuous process" (9.2.2, L17113); phase 4 "Risk Monitoring – Determine effectiveness of applied mitigation and manage accordingly." (L17129)
> Configuration management: "The security goal of configuration management is to know that a change occurred and what was changed. Changes should trigger a risk assessment ... If the change is major, it may be necessary to reanalyze some of the security aspects of the system." (9.3 "Configuration Management", L17801-17807)
Relevance: strong text support for per-change security checks in CI. HB901's own words: "continuous", "changes should trigger a risk assessment".

### Separation of duties (relevant to who sees and edits findings)
> "Development staff does not have access to production data, unless specifically authorized by the functional data owner to repair a limited number of records" (9.3.2.1, L17339-17340)
> "Access to system logs and system audits are limited to the system security analysts, and all such access is reviewed by IS management" (L17361-17362)
> Table 49: "The separation of duties is able to be demonstrated to, or validated by, an outside party." (L17399)
Relevance: the dashboard and evidence ledger should enforce role separation: vendor developers can submit evidence but cannot mark their own security findings closed; state security owns closure. Keep the ledger append-only with audit logging.

### Audit trails
> Audit trails capture "Successful and unsuccessful login attempts", "Actions taken by system administrators and security personnel", "All administrative actions performed on a system", each with "Date and time of event", "Type of event", "Success or failure" (9.4.8, L18097-18117). "Audit trail logs are properly secured with access limited to system administrators. The audit logs should be reviewed regularly. States must establish and adhere to a policy for length of retention." (L18119-18120)
Apply to the dashboard itself.

### Identification/authentication
> "all user IDs must be unique throughout the system ... Systems may require the use of a biometric/smartcard, digital certificates, a public key infrastructure (PKI), or a token ... Single Sign-On mechanisms provide additional security during log-in." (9.4.1.1, L17846-17850)
> "Supervisors and managers continuously assess the privileges granted to employees and contractors." (L17827-17828)
State SSO fits.

### Penetration testing
> "As part of the security assessment for IS, penetration testing is incorporated to effectively evaluate the security posture of the network and IS. ... Once all the vulnerabilities are found, they are documented along with the mitigation strategies to resolve all discovered vulnerabilities." (9.4.7, L18080-18086)
No frequency or independence requirement stated.

### PII in testing
> "Organizations often use PII for testing new applications ... The use of PII in testing, research, and training increases risk of unauthorized disclosure or misuse of the information. If PII must be used, organizations take measures to minimize any associated risks and to authorize the use of and limit the amount of PII for these purposes." (9.5.3, L18419-18425, quoting NIST)
> "Contractors and service providers, along with government personnel, should be required to adhere to the relevant governance and controls." (9.5.2, L18395-18396)
Relevance: CI connectors must not pull PII into the evidence ledger; store test results and hashes, not case data. Snowflake connector needs care.

### Silent topics
Ch9 has no text on cloud hosting, FedRAMP, GovCloud, or on tools that store security findings. Security findings are "sensitive" by implication only (security plan is a "status report" to FNS). Treat the dashboard as a system that holds sensitive security information under the state's security plan; handle access with least privilege. HB901 gives no FNS-specific rule that forbids AWS GovCloud.

---

## Appendices — list and relevance

From the TOC (L860-1060):
- A1 Acronyms and Glossary; A2 Regulations; A3 Regional Office info; A4 System Type and Acquisition Selection Tool (incl. COTS, cloud/SaaS); A5 Feasibility Study Worksheet; A6 Cost Benefit Analysis Worksheet; A7 Sample Transmittal Letter (+ checklist); A8 Sample Budgets; A9 State Sole Source Exception Request.
- **A10 Request for Proposal Template** (L21509+) — includes ownership clauses (cross-ref A16).
- **A11 Federal Procurement Clauses** — A11.6 "Royalty Free Rights to Use Software or Documentation Developed" (L23718).
- **A12 RFP and Contract Review Checklist** — what FNS looks for in RFPs/contracts; testing, acceptance, royalty-free rights rows.
- **A13 Sample Status Report** — sections A13.1-A13.16 incl. Deliverable Status, Open Risks (risk register), Budget vs Actual, Contractor Performance Update.
- **A14 Security Plan Checklist** — Management, Operational, Technical, Privacy, EBT controls.
- **A15 Final Test Plan Template** — A15.2 (scope, schedule, staffing, entry/exit, pass/fail, defects, regression, data conversion, security, stress/load) and A15.3 (UAT deliverables, Go/No-Go, roll back).
- **A16 Ownership Rights** — policy, clauses, MOSA, inappropriate IP clauses, free software, private development.

### A11.6 (L23718-23740) — 2 CFR 200.315
> "(b) The non-Federal entity may copyright any work that is subject to copyright and was developed, or for which ownership was acquired, under a Federal award. The Federal awarding agency reserves a royalty-free, nonexclusive and irrevocable right to reproduce, publish, or otherwise use the work for Federal purposes, and to authorize others to do so."
> "(a) ... The non-Federal entity must use that property for the originally-authorized purpose, and must not encumber the property without approval of the Federal awarding agency."

### A12 checklist rows (testing, acceptance, rights)
> "State's requirements for • Federally compliant testing and live pilot • Phased implementation • Caseload conversion • Uninterrupted service to users and/or clients" (L23905)
> "Require a test plan including, but not limited to: unit testing, integration testing, performance testing, end-to-end testing, UAT, and regression testing, live pilot" (L23951)
> Section E Inspection and Acceptance: "Plan for State agency review and approval of work performed", "System acceptance requirements", "Quality Assurance Surveillance Plan (QASP) • State the review and approval period for each deliverable" (L24017-24020)
> "Contract and Administrative Deliverables • Type and frequency of expected project status reports" (A12, L23974)
> Contract clauses include "Royalty-Free Rights to Use Software or Documentation Developed" and "Turnover provision or non-transferability" (A12 L24156, L24180)

### A13 Sample Status Report
Checklist (L24380-24391): "Executive Summary | Work Accomplished | Deliverables in Progress | Planned Activities | Project Deliverables Status | Project Budget and Actual Expenditures | Updated Project Schedule of Milestones and Deliverables (Gantt Chart) | Contractor Performance Update".
> A13.15: "this optional information is used to assist other states when FNS is asked about contractor performance" (L24681-24682)
> A13.16: "Actual updates to the project schedule of milestones and deliverables will be reported in the appropriate APDU." (L24687-24688)
No frequency stated in A13. No operational metrics section.

### A15 Final Test Plan Template — items beyond ch6
> A15.3.1 UAT deliverables to FNS: "UAT Test Plan (if modified since last shared with FNS) • UAT Test Results and Report • UAT Test Procedures • UAT Test Cases and Scripts (upon request) • UAT Report on Open Risks • UAT Report on failures with severity levels" (L26192-26204)
> A15.3.2: "The process is performed a minimum of twice during the system lifecycle, once after completing UAT and again after completing the Pilot. FNS concurrence with UAT results allows for the project to proceed from UAT to Pilot and the continuation of funding. FNS approval of Pilot results allows for the project to proceed from Pilot to Rollout and the continuation of funding." (L26211-26220)
> "The Go/No-Go decision is not a test; however, the basis of this determination is derived from the UAT test results and the Pilot test results. Go/No-Go criteria are not the same as Entry/Exit Criteria" (L26221-26222)
> A15.3.3: "The roll back contingency plan should include the specific targets or metrics that must be met during conversion or rollout before the state can proceed – incremental go/no-go points. Failure to meet these targets will trigger the need to stop the pilot and roll back to UAT, or to stop the conversion or rollout and return to pilot." (L26238-26241)
> A15.2.4.1 Table 59 (L25620-25638): "Test Leads | Contractor Team, State Agency staff | Authority and accountability for all work performed by the specific Test Teams (e.g., functional, integration, performance, UAT). Primary responsibility for the Test and Acceptance Plan, Test Cases, Test Scripts and Expected Results, Defect Tracking Report, User Acceptance Function Test (UAT), Stress Test, Acceptance Reports, and Pilot Quality Acceptance Report deliverables." and "Tester | State Agency staff | Follow test scripts, as written". "Test Manager | State Agency Management".
> "The test environment should replicate the production system as closely as possible." (A15.2.4.2, L25646)
> "The timeline will need to have multiple functional iterations if an agile development process is being used." (L25564)
Relevance: contractors can co-lead UAT; state staff execute UAT scripts; state management runs the test. Incremental go/no-go points during rollout are explicitly allowed. Metrics-based rollback triggers are a natural rule-engine use.

### A16 Ownership Rights (L26251-26976) — key for licensing
> "There are several policy requirements that State or local governments must include in all contracts for any software or software modifications and associated documentation that is designed, developed, or installed with Federal financial participation funding. These include ownership rights and a broad Federal License" (A16.1, L26255-26258)
> 7 CFR 277.18(l)(ii) quoted: "FNS reserves a royalty-free, nonexclusive, and irrevocable license to reproduce, publish or otherwise use and to authorize others to use for Federal government purposes, such software, modifications and documentation [designed, developed or installed with Federal funds]." (L26260-26263)
> "Proprietary vendor software packages and operating systems (OS) that are provided at established catalog or market prices and sold or leased to the public are not subject to these ownership provisions. Federal funding is not available for proprietary applications software developed specifically for SNAP or WIC." (L26265-26267)
> "The RFP and contract must make it clear that the source code, documentation, database schema, and other supporting components must be made available by the State and/or Vendor to other State agencies for Federal government purposes such as system analysis and/or transfer." (L26269-26271)
> "State ownership of software designed, developed, or installed with FFP means the State agency should secure copyright ownership from the vendor or developer through specific contract clauses." (A16.2.3, L26315-26317)
> Example clause "State Ownership": "All Deliverables and modifications, in whole and in part, shall be deemed works made for hire of <the jurisdiction> ... copyright shall belong solely to <the jurisdiction>." (A16.3.2, L26552-26553)
> Example clause "Federal License": "All appropriate State and Federal agencies (including without limitation the Federal government agencies providing Federal financial participation) shall have a royalty free, nonexclusive, and irrevocable license to reproduce, publish, translate or otherwise use and to authorize others to use for Federal government purposes all materials, the software and modifications thereof, and associated documentation designed, developed, or installed with Federal financial participation under this Agreement." (L26572-26576)
> "Ownership of Preexisting Products": "The Vendor will retain all right, title and interest in and to all Property developed by it, 1) for clients other than <the jurisdiction>, and 2) for internal purposes and not yet delivered to any client ... prior to the date of the contract." (L26593-26596)
> A16.5.1: "States should avoid any language that implies that the deliverable provides for anything other than the State's complete and exclusive ownership. For instance, language that implies that the software is being licensed to the State by the vendor should be avoided. A request to sign an end user license agreement (EULA) or to pay ongoing license fees indicates that the State is not receiving absolute ownership." (L26874-26878)
> A16.5.2: "Any language that states or implies that the State is limited in what it may do with the deliverable is objectionable. ... The State is free to grant, sell, or license the software however it wants. Any language that implies the State must seek permission from the vendor for the deliverable, excluding third party components identified elsewhere in the contract, is suspect" (L26884-26889)
> A16.2.7: "Public domain software is ... the complete absence of copyright ownership ... 'Public domain' may be used incorrectly to refer to any software distributed under a free software license. ... the copyright (or other rights) to the software may still be held by the author." (L26431-26441)
> A16.6.1: "States do have the discretion to avoid holding copyrighted works, or to dispose of the copyright and put the software in the public domain. ... FFP eligibility requires that the State obtain ownership of the copyright in order to transfer the required non-exclusive license to the Federal awarding agency." (L26900-26910)
> A16.6.2-6.3: States may license State-owned copyrights back to vendors and charge fees; "States should be aware of vendors' intentions to profit from works developed at public expense" (L26920-26937)
> A16.7: "FNS is entitled to the Federal License in software only if FNS funds are used to develop the software, or if a State uses FNS funds to purchase copyright ownership of privately developed software." (L26959-26960) and "State use of FNS funds simply to lease contractor-developed software would not give FNS such royalty-free use." (L26956)
> A16.8: "Offers of free, or practically free, software should be rejected if acceptance thereof would give the offeror an unfair competitive advantage as to subsequent hardware procurement or follow-on software. This would be equal to receiving a gift from an interested party, or would be an unauthorized barter arrangement rather than a gift." (L26964-26967)
> A16.9: "Any time (prior to contract award or during contract performance) that a contractor offers or proposes to pay for part of the development costs, a red flag should be waving. ... software not paid for by the State may not be covered by transfer, assignment, copyright, or ownership provisions in the contract." (L26971-26976)
> A16.4 RFP instruction: "The Offeror shall justify any use of proprietary, vendor-unique, or closed components" (L26622)

**What this means for a noncommercial license on the toolkit:**
1. If any part of the toolkit (rules, connectors, ledger, dashboard, or state-specific config) is built or modified under the state's contract with FFP, the state must own the copyright and FNS (and CMS) get a royalty-free federal-purpose license. A vendor-held noncommercial license on those parts conflicts with A16.5.1/A16.5.2 and risks FFP.
2. If the toolkit is pre-existing and privately funded, the vendor may keep it ("Ownership of Preexisting Products"). But the state then leases rather than owns it, FNS gets no federal license (A16.7), and the RFP should require justification of "proprietary, vendor-unique, or closed components" (A16.4).
3. If the toolkit owner is the DDI vendor or a bidder and offers it free, A16.8 (free software giving "unfair competitive advantage as to ... follow-on software") and A16.9 (contractor paying for part of development is a "red flag") apply.
4. HB901 does not speak to open-source licenses as such. A permissive or copyleft OSI license is not barred. A noncommercial clause is a restriction on use that, under 277.18(l), cannot bind the state or federal government for FFP-funded parts, and it would block other states' contractors (commercial actors) from using it, which undercuts the reuse goal in 5.5.1 and SHO 25-003's AoA reuse step.
5. CMS parallel (not re-read here): 45 CFR 95.617 and CEF05/CEF06 have the same structure.

---

## Answers to the seven questions

### 1. Testing, UAT, pilot, rollout, Go/No-Go (beyond ch6)
- FNS can do a "System Functional Requirements Review after the system has passed UAT, before the pilot, or before the deployment of software ... may be conducted by reviewing UAT or Pilot Evaluation documentation" (7.5.2).
- SIRT is used "prior to User Acceptance Testing, and again after statewide implementation"; "FNS will use this same tool for UAT, pilot, and possibly post-implementation reviews" (5.3.1.4).
- "Use a phased approach o Avoid a 'big bang' approach"; "Provide documentation of the pilot evaluation to FNS"; "Complete testing before starting a rollout" (7.1.1).
- FNS "reserves the right to ... participat[e] in User Acceptance Testing (UAT)" (7.5.2).
- RFP should require "an incremental system demonstration every few months during development" and CM software (4.6.1).
- A15.3.2: Go/No-Go at least twice; "FNS approval of Pilot results allows for the project to proceed from Pilot to Rollout and the continuation of funding."
- A15.3.3: rollback plan with "incremental go/no-go points" based on "specific targets or metrics".
- A12: RFP should state "Federally compliant testing and live pilot".
- Ch5: parallel runs happen before pilot, "does not occur during pilot testing".

### 2. Ongoing FNS oversight after rollout — belief mostly confirmed, with three corrections
Confirmed: HB901 has no recurring operational metric reporting like CMS's monthly ORW. "FNS does not require annual APD Updates to approve the funding of maintenance and operations activities" (1.5.1.3). CBA is not tracked "beyond initial approval of the IAPD" (5.3.3). Status reports have no set frequency (7.5.1).
Corrections / nuances:
(a) Biennial security review with written summary and action plan to FNS (9.7; 7 CFR 277.18(m)(3)) is a recurring post-rollout obligation.
(b) Post-implementation review "preferably six months after implementation and rollout" (7.6), plus FNS "Arranging dates and preliminary agenda for post-implementation reviews and preparing final reports, including any corrective action requirements" (1.8.1), and a possible SIRT review "once it is fully operational statewide" (5.3.1.4; 7 CFR 277.18(g)(2)). These are one-time, not periodic.
(c) A final APDU and APD closure (1.7.3). M&O enhancements that add function need an IAPD (1.5.1.3); all SNAP contract amendments go to FNS for records (4.2.4.3).
Also: FNS "accesses data and State IS and uses reports generated by State IS to meet federal reporting requirements" (1.9.2) — this is program reporting outside the APD process (not covered in HB901 detail).

### 3. Procurement/contract requirements
- Thresholds: SNAP RFP/contract ≥$6M competitive; ≥$1M non-competitive; amendments >20% cumulative of base (Tables 16-17). Separate copies to FNS and HHS (4.3.2).
- Must include: 277.18(l) ownership + federal license (4.7.7.6, 4.10, A16); 2 CFR 200 App. II clauses (Table 20, A11); access to records and all aspects of the IS (4.7.7.5).
- Recommended: CM software, requirement sign-offs, change control, incremental demos, source code with comments (4.6.1); payment after state acceptance of each major deliverable (4.7.8); holdbacks e.g., 20% until accepted/certified (4.7.2); QASP (recommended, not required, 4.7.4); test plan incl. UAT, regression, live pilot (A12); transfer/reuse package deliverable (5.5.1.2).
- Escrow: mentioned only as a common performance tool (4.7.2). Not required.
- Open source: not addressed directly. A16 explains free software licenses keep copyright with the author; free software from an interested party may be rejected (A16.8).
- No licensing restriction may limit the state's use of FFP-funded deliverables (A16.5).

### 4. Agile / iterative / incremental
- Methodology-neutral: "waterfall, iterative, spiral, agile, etc." (5.4.3); if agile is preferred "these should be stated in the RFP".
- "incremental system demonstration every few months" (4.6.1); RFP should state how "detailed requirements may be added later, depending upon the development methodology" (4.9.1).
- Test timeline "will need to have multiple functional iterations if an agile development process is being used" (A15).
- Limits: cumulative threshold for "incremental efforts" (1.5.1.1); "Incremental or limited funding" is listed as a risk (7.4.3.1); FFP contracts preferred, T&M discouraged (4.8.1); changes need APDU approval before costs, no retroactive approval (7.4.3.3).

### 5. Security
- State chooses standard; FISMA/NIST recommended (9.1, 9.1.1). Applies to systems "being developed, implemented, and tested" (9.1).
- Biennial review + written summary + milestone action plan to FNS (9.7).
- Continuous risk assessment; changes trigger risk assessment (9.2.2.1, 9.3 Configuration Management).
- Separation of duties, demonstrable to outside party (9.3.2.1, Table 49); audit trails with retention policy (9.4.8); unique IDs, SSO acceptable (9.4.1.1); pen test findings documented with mitigations (9.4.7); minimize PII in testing (9.5.3).
- Nothing on cloud/GovCloud/FedRAMP or on tools that hold security findings.

### 6. SHO #25-003
- Changes: MES APD template (all types except Operational), MES OAPD template (M&O), MES MDBT+CHIP template, updated Operational Report Workbook and MES Data Submissions and Intake Procedures Manual, AoA template (Section 5 of MES APD / Appendix A of OAPD), Project Status Report template, RFP checklist, SMC Intake Form for all modules incl. EVV; EVV OBC sunset.
- Monitoring: monthly ORW uploads to CMS repository; OAPD attestation of ORW location; monthly project status reports for states pursuing certification; reporting from go-live date. Non-submission = non-compliant, could lose enhanced FFP.
- Effective: transition "within 6 months of the Paperwork Reduction Act (PRA) approval" (date not in letter).
- Supports the toolkit: SMC "emphasizes metric data and operational reporting rather than checklists"; "standardizing data submission formats"; "allowing states to update the viability and value of their metrics"; status template gives "consistent, structured data". Certification evidence still judged as "Evidence Satisfactory / Not Satisfactory".
- Constrains/contradicts: submissions are files (workbooks, templates) uploaded to a CMS repository, not live feeds; CMS defines the formats, so the toolkit must export to CMS templates rather than replace them. Certification still needs ≥6 months in production (stated under EVV bullet but the SMC guidance has the same rule). No mention of SNAP.

### 7. Assumptions to check
- "One combined APD goes to both agencies": Not supported. HB901: "in joint projects, State agencies must submit APDs to all federal agencies" and "Each federal agency is responsible for review and approval of its own costs" (1.1, 1.9.4.1); RFPs/contracts: "separate copies must be submitted to FNS and ... DHHS" (4.3.2). SHO 25-003's "combined" means MMIS + E&E in one CMS APD, not CMS + FNS. A single document may be sent to both, but there are two submissions and two approvals under two rule sets.
- "Pilot must be live with the new system as system of record": Supported in substance. A12: "Federally compliant testing and live pilot" and test plan "live pilot"; ch5: parallel processing "does not occur during pilot testing, but does occur in earlier project phases"; A15.3.2: FNS approval of pilot results before rollout. HB901 in these chapters does not use the words "system of record" (ch5 asks "Which system contains the official record during concurrent operations?" as a planning question). Ch6 remains the main source.
- "A contractor may not perform UAT or the pilot": Not supported as stated. A15 Table 59 shows "Contractor Team, State Agency staff" as Test Leads with responsibility for UAT and Pilot acceptance deliverables; "Tester | State Agency staff"; "Test Manager | State Agency Management". The real limits are: (i) conflict of interest — the builder cannot evaluate its own work or set the performance measures it is judged by (4.8.6, Table 22); (ii) QA/IV&V must be separate firms (4.8.5.5, Table 22); (iii) SNAP client-contact tasks are for State merit staff unless FNS approves (5.2.4), which matters for a live pilot; (iv) the State keeps decision authority and federal communications (4.8.5.2), and makes the Go/No-Go recommendation (A15.3.2).

---

## Changes the proposal should make

1. Show two federal tracks. Say the state submits the APD (and RFPs, contracts, amendments) to FNS and to CMS, and each approves its own share. Do not say "one combined APD" approved jointly. The toolkit can generate both packages from one ledger.
2. Correct the "no FNS post-rollout reporting" claim. Say: FNS has no monthly metric workbook, but it has a biennial security review summary and action plan (7 CFR 277.18(m)(3); HB901 9.7), a post-implementation review about six months after rollout (7.6), a possible SIRT review once statewide (5.3.1.4), a final APDU and APD closure (1.7.3), and IAPDs for new functionality in M&O (1.5.1.3).
3. Map the toolkit to FNS's named review points: SIRT before UAT, System Functional Requirements Review (after UAT/before pilot/before deployment, can be a desk review of UAT and pilot evidence), the two Go/No-Go decisions, the rollback "incremental go/no-go points", and the PIR.
4. Fix the license plan. Any toolkit part built or changed with FFP must be state-owned with a federal royalty-free license (7 CFR 277.18(l); A16). A noncommercial license cannot restrict the state or federal agencies for those parts. If the core toolkit is pre-existing and private, say so, list it as a pre-existing product, and accept that FNS gets no federal license (A16.7). Avoid offering it free if the owner is a bidder or the DDI vendor (A16.8, A16.9). Consider a permissive OSI license so other states and their contractors can reuse it; this matches FNS reuse policy (5.5.1) and the AoA reuse step in SHO 25-003.
5. Put the state, QA, or IV&V in charge of the rules catalog thresholds and the pass/fail judgment. The DDI vendor can feed evidence but cannot judge its own work or set its own measures (4.8.6, Table 22). Frame the rules + ledger as the machine-readable part of the state's QASP (4.7.4) and RTM (7.4.1).
6. Drop or reword "contractor may not perform UAT or pilot". Say: state staff execute UAT scripts and run Go/No-Go; contractors may co-lead testing (A15 Table 59); live pilot client-contact work must use merit staff unless FNS approves (5.2.4).
7. Add contract language hooks: payment after state acceptance of each increment with evidence (4.7.8, 4.7.2), CM software and change control (4.6.1), incremental demos (4.6.1), access to records and systems (4.7.7.5), a transfer/reuse package that includes test cases and scripts (5.5.1.2), and "SHALL" wording.
8. Address agile within FNS limits: cumulative thresholds still apply (1.5.1.1); scope/cost/schedule changes need APDU approval before costs (7.4.3.3); FNS prefers fixed-price (4.8.1). Tie payment points to accepted increments.
9. Security: cite HB901's own "continuous" risk assessment and change-triggered review (9.2.2.1, 9.3 Configuration Management) as the basis for CI security checks. Build separation of duties, unique IDs, SSO, and audit trails into the dashboard (9.3.2.1, 9.4.1, 9.4.8). Keep PII out of the ledger (9.5.3). Note HB901 is silent on cloud/GovCloud; rely on the state security plan and CMS ARC-AMPE.
10. SHO 25-003: export to CMS templates (MES APD/OAPD, ORW, Project Status Report, SMC Intake Form, RFP checklist) rather than replace them. Note monthly ORW from go-live and monthly status reports. State the effective date as "6 months after PRA approval" and look up the PRA approval date. Use the AoA reuse step as a reason to keep the toolkit openly reusable.

## Not read / limits
- HB901 chapters 2, 3, 6, 8 were not re-read (per instructions). Some answers (pilot as system of record, ch6 Go/No-Go detail) rely on those earlier reads.
- Appendices read in part: A11.6, A12 (testing/acceptance/rights rows), A13 checklist and A13.15-16, A15.2.4 and A15.3, A16 in full. A1-A10, A14 body, and most of A12/A13/A15 were only skimmed via TOC and grep.
- Chapter 9 sections 9.4.2-9.4.9 (logical access, OS, network, firewalls, routers, virus, web, mobile) and 9.6 (EBT controls) were skimmed by grep, not read line by line. No FNS-specific rule on cloud, FedRAMP, or POA&M was found by search.
- SHO 25-003: full text read (7 pages). The PRA approval date for CMS-10536 templates is not in the letter and was not looked up.
- The handbook markdown is a PDF conversion; some table cells are garbled. Quotes from tables were checked against surrounding text but may contain conversion artifacts.
