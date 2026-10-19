MSE800 / ASSESSMENT 2 / OBJECT-ORIENTED PROJECT

Project Report

Campus Equipment Loan System

Xuerui Huang, Bin Wang and Yonghui Dai

Classroom simulation with verified technical evidence. The report develops a complete example of client needs, short sprints and reflection. Those activities have not been carried out by the students. The software, assistant-run checks and newly recorded assistant Git baseline are actual artifacts. No client, Kaiārahi or community endorsement is claimed.

1. Project purpose and scope

The case concerns a campus equipment desk lending a laptop, camera and projector. The operator needs to see availability, register a loan and record its return without losing earlier records. The product is a local Python terminal application with SQLite storage, suitable for demonstrating a small object-oriented system.

The scope includes availability, borrowing, return, history, persistence and Unicode aliases. Online booking, accounts, payments, fines and deployment are excluded. Demonstrations use fictional aliases because the prototype has no login, access controls or database encryption.

2. Team responsibilities

| Member | Assigned responsibility | Presentation |
| --- | --- | --- |
| Xuerui Huang | Requirements, coordination, menu interface, priorities, cost and report integration. | Scope, requirements, teamwork and cost. |
| Bin Wang | Domain objects, borrowing/return rules, integration and demonstration. | Object-oriented design and product demo. |
| Yonghui Dai | SQLite persistence, tests, evidence, consultation preparation and reflection coordination. | Testing, cultural considerations and reflection. |

Client-role arrangement for the written scenario

The client persona is the Equipment Desk Operator. In the suggested classroom rehearsal, Bin reads that persona while Xuerui gathers requirements and Yonghui records decisions; Bin then returns to the developer role. This keeps the exercise manageable for three people. It is an internal role-play, not independent acceptance or a confirmed client-team arrangement. Use the tutor’s required client arrangement for assessed activity.

Working agreement and case timeline

Share agendas, invite each person’s view, allow written follow-up and check decisions together. Review another component before integration. Day 1: kickoff. Day 2: requirements and consultation preparation. Days 2-5: Sprint 1. Days 6-9: Sprint 2. Day 10: package and presentation rehearsal. The 54-hour allocation is a scenario estimate, not an attendance or timesheet record.

3. Requirements and acceptance criteria

The six stories define the completed prototype’s scope. Priorities are justified by business value in the case; they are not evidence of actual client agreement.

US01 | View equipment | Must

As an operator, I want to see equipment availability so that I can respond to a loan request.

Acceptance: Each item shows a unique ID, name and correct Available or On loan status.

US02 | Borrow equipment | Must

As an operator, I want to record a loan so that equipment use is tracked.

Acceptance: A valid device ID and alias create one active loan. Reject unavailable or unknown devices and blank, overlong or non-printable aliases without adding a record.

US03 | Return equipment | Must

As an operator, I want to register a return so that the device can be lent again.

Acceptance: Returning an active loan records a timestamp and restores availability. Reject unknown or already returned loans; keep the history.

US04 | View history | Should

As an operator, I want loan history so that I can check previous and current use.

Acceptance: Show loan ID, device, alias, borrowing time and active/returned status. Explain when no records exist.

US05 | Keep records | Must

As an operator, I want saved records to survive a restart so that loan information is not lost.

Acceptance: Reopening the same database preserves history and availability without duplicating the seed equipment.

US06 | Preserve names | Must

As a user with macrons or other Unicode characters in my alias, I want them preserved so that my alias is represented accurately.

Acceptance: Save and retrieve a fictional alias such as Māia unchanged, including after restart. Do not request ethnicity or contact details.

Priority rationale: US01-US02 support the initial loan decision; US03 completes the cycle. US05 prevents lost records and US06 preserves the entered alias. US04 is a Should item for checking earlier activity, although it is implemented in the prototype.

Local impact: this is an undeployed classroom prototype using fictional data. Direct community impact has not been established. Before real campus use, gather affected users’ language, access and data needs and revise priorities with appropriate guidance. A Unicode test alone cannot establish cultural acceptance.

4. Object-oriented design and specification

[Diagram: menu -> LoanService -> EquipmentRepository -> SQLite; Equipment and Loan objects carry data.]

The menu delegates operations to LoanService, which receives an EquipmentRepository through its constructor. This composition keeps SQL outside the interface. Equipment and Loan are immutable data classes. A class hierarchy for different equipment types would add complexity without supporting a current requirement.

| Component | Implemented responsibility |
| --- | --- |
| app.py | Terminal menu, input conversion, result display and operational input/database error messages. |
| models.py | Equipment: ID, name and availability. Loan: ID, equipment, alias and borrowing/return timestamps. |
| service.py | Alias and equipment validation, one-active-loan rule, creation and valid returns. |
| repository.py | SQLite schema, fixed seed inventory, queries and committed writes. |

Data model and integrity

equipment stores id and name. loans stores id, equipment_id, borrower, borrowed_at and returned_at. The foreign key links a loan to its device; a null returned_at identifies an active loan. Availability is derived from active loans so it cannot disagree with a separately stored flag.

A partial unique index prevents more than one active loan for a device. Service validation produces a clear message, while the index protects the stored constraint. Queries use SQL parameters. Returning a loan sets its timestamp and keeps the record.

Operating specification

| Requirement | Specification |
| --- | --- |
| Runtime | Python 3.10+ with sqlite3, a terminal and a writable local folder; one operator in the case. |
| Alias | Trim surrounding whitespace; require 1-80 printable characters. Use fictional values for demonstrations. |
| Identifiers / time | Device and loan IDs are integers. Unknown IDs are rejected. SQLite timestamps use UTC. |
| Storage | Default equipment.db beside app.py; --db selects another file. Fixed seed IDs prevent duplicate inventory. |
| Failure handling | Invalid menu or numeric input returns to the menu. Database errors during operations are shown. Startup recovery and damaged database repair are not validated. |

Inventory is fixed. There is no login, encryption, deletion/retention workflow, reservation engine or shared-service security assessment. These limits keep the classroom scope small.

5. Client kickoff and requirements records

SIMULATED CASE RECORD. Relative days, discussions and role outcomes below form a written classroom example. They are not records of meetings attended by the named students.

M01 | Day 1 | Kickoff | 25-minute example

Role allocation: Xuerui facilitates; Bin reads the fictional operator’s needs; Yonghui records actions. Agenda: current loan workflow, users and data, priorities, cultural considerations, acceptance and next steps. Each role has time to question an assumption.

Client-role brief: an operator should answer whether a device is available, record a loan without double-lending, and later return it. The case assumes a small fixed inventory and one workstation. A spreadsheet-like list was considered, but explicit loan records were chosen to retain history.

| Decision | Reason / agreed scenario action | Owner |
| --- | --- | --- |
| D01: limit scope | Local terminal; three devices; no accounts, reservations or online deployment. | Xuerui |
| D02: minimise demo data | Fictional alias and timestamps only; no contact or ethnicity fields. | Yonghui |
| D03: observable quality | Reject duplicate active loans and preserve data across restarts. | Bin |
| D04: cultural review | Prepare an appropriate advisory route and questions before treating cultural criteria as settled. | All; Yonghui records |

M02 | Day 2 | Requirements | 20-minute example

| Question from the team | Answer supplied by the fictional operator role |
| --- | --- |
| How should a return identify the record? | Use the displayed Loan ID. A device ID identifies equipment, not a particular borrowing event. |
| Should a returned record disappear? | No. Keep the alias and timestamps so current and previous loans can be reviewed. |
| Which features matter first? | Availability, borrowing, return and persistence; preserve entered aliases throughout. History supports follow-up. |
| Is a web interface necessary? | A terminal is enough for this demonstration. Reconsider access needs before actual use. |
| How will the result be checked? | Link every story to observable tests, demonstrate the full workflow and keep cultural review separate. |

Actions and culturally informed practice

Xuerui consolidates US01-US06 and the scope; Bin checks the service rules; Yonghui links tests and data fields. In this example, written follow-up is available and the facilitator repeats the ID distinction before closing. Partnership is an open advisory action, participation shapes the meeting method, and protection informs the use of fictional data. Actual consultation remains outstanding.

6. Sprint 1 and first review

SIMULATED CASE RECORD. Relative days, discussions and role outcomes below form a written classroom example. They are not records of meetings attended by the named students.

Goal, Days 2-5: review inventory, borrowing, storage and alias handling. This effort allocation also includes the Day 1 kickoff. The sequence illustrates development and review of the reference product; it is not reconstructed student history.

| Task / story | Owner / hours | Scenario result |
| --- | --- | --- |
| S1-01: Kickoff and requirements | Xuerui / 5 | Scope, six stories and questions recorded. |
| S1-02: Inventory/borrow menu; US01-US02 | Xuerui / 3 | Equipment selection and success/error messages reviewed. |
| S1-03: Objects and borrow rules; US02 | Bin / 6 | Models, alias validation and duplicate protection reviewed. |
| S1-04: Cross-component peer review | Bin / 1 | Menu/service/storage boundaries checked. |
| S1-05: Storage foundation; US05 | Yonghui / 5 | Schema, fixed seeds and active-loan index reviewed. |
| S1-06: Initial checks; US01-US02-US06 | Yonghui / 2 | Inventory, invalid/duplicate requests and macrons mapped to tests. |
| S1-07: Cultural preparation | Yonghui / 1 | Consultation brief prepared; no adviser acceptance claimed. |

M03 | Day 5 | Client-role review | 20-minute example

The review demonstrates available inventory, a successful loan and rejection of a second active loan. The operator role asks how to identify the correct loan at return and whether previous borrowing records remain visible.

| Feedback | Case decision | Requirement / check |
| --- | --- | --- |
| CF01: avoid double-lending | Retain both service validation and the database index. | US02 / AT03 |
| CF02: identify the right loan | Retain the displayed Loan ID and explicit return prompt. | US02-US03 / AT02, AT05 |
| CF03: keep earlier records | Preserve return timestamps and show record status. | US03-US04 / AT05, AT07 |

Retrospective and action

The example exposes a communication risk: “equipment ID” and “loan ID” can be used interchangeably in discussion. Xuerui standardises those terms in the demonstration; Bin checks the operation from menu to service; Yonghui adds the explicit return step to the review. This is a scenario improvement to explanation, not a claim that a previously observed software defect was repaired.

Effort model: Xuerui 8 h + Bin 7 h + Yonghui 8 h = 23 person-hours. The review outcome is recorded only within the simulation.

7. Sprint 2 and final client-role review

SIMULATED CASE RECORD. Relative days, discussions and role outcomes below form a written classroom example. They are not records of meetings attended by the named students.

Goal, Days 6-9: complete the return/history explanation, review persistence and input handling, and prepare acceptance. This effort allocation also includes final packaging and rehearsal on Day 10.

| Task / story | Owner / hours | Scenario result |
| --- | --- | --- |
| S2-01: Return/history menu; US03-US04 | Xuerui / 2 | Loan ID prompt and record status reviewed. |
| S2-02: Cost and report integration | Xuerui / 4 | 54-hour plan and story/decision links reconciled. |
| S2-03: Workflow checks and rehearsal | Xuerui / 4 | Operator steps and explanations rehearsed in the case. |
| S2-04: Return rules; US03 | Bin / 2 | Unknown/repeated returns rejected; history retained. |
| S2-05: Integration, design and review | Bin / 9 | Integration 3 h; design explanation 3 h; review/rehearsal 3 h. |
| S2-06: Acceptance checks | Yonghui / 3 | Story-to-test mapping and acceptance status reviewed. |
| S2-07: Evidence, culture and reflection | Yonghui / 7 | Evidence/rehearsal 3 h; reflection/presentation 4 h. |

M04 | Day 9 | Final review | 25-minute example

The operator role observes borrow, duplicate rejection, return, history and restart. Within the scenario, this covers the agreed local workflow. The role then asks for online booking. The team defers it because booking introduces dates, conflicts and further access decisions beyond the baseline.

| Acceptance item | Worked-example disposition |
| --- | --- |
| US01-US06 | Scenario workflow accepted by the fictional operator role. Actual technical results are recorded separately in section 11. |
| CF04: online booking | Deferred to a later iteration; not implemented or included in the NZD 1,815 baseline. |
| Cultural / operational acceptance | Open. No adviser review, community acceptance, real-data approval or deployment sign-off is represented. |

Retrospective and next iteration

The scenario review checks the previous action by returning the displayed loan rather than entering the device ID. A remaining weakness is dependence on one computer and one demonstrator. The next rehearsal should use the final extracted ZIP on the presentation computer, and each member should explain one component owned by another member.

Effort model: Xuerui 10 h + Bin 11 h + Yonghui 10 h = 31 person-hours. Combined total: 54 h, with 18 h per role. These are estimates, not measured student effort.

8. Kaiārahi consultation preparation

Status: prepared; consultation not conducted. No Kaiārahi or Māori representative supplied the material below. It is a complete team briefing and question set, not attributed advice or a simulated endorsement.

Purpose and proposed arrangement

Yonghui coordinates the request through the tutor; Xuerui explains scope and requirements; Bin demonstrates the workflow. A short briefing would show fictional-data borrowing and return, then ask which perspectives and acceptance criteria are appropriate. Ask how guidance may be recorded and whether follow-up or compensation arrangements apply.

| Question for an appropriate adviser | Current team position to discuss |
| --- | --- |
| Who should participate and whose needs are relevant? | Identify affected users and an appropriate advisory route. An internal operator persona cannot stand for Māori perspectives. |
| Are names and interface wording suitable? | Preserve Unicode aliases, including macrons. Do not introduce unverified translations or cultural imagery. |
| What data is needed, and how should it be handled? | Use fictional aliases now. Real use would require agreed purpose, access, retention and protection measures. |
| Could the workflow exclude users? | Demonstrate keyboard/terminal interaction and invite spoken or written feedback on barriers. |
| What would acceptable outcomes look like? | Agree observable review criteria and record how advice changes or confirms requirements. |

Te Tiriti principles in the preparation

Partnership: seek input before treating requirements as culturally settled. Participation: provide a clear demonstration and different ways to contribute. Protection: minimise demonstration data, preserve entered names and review any cultural content. These are project proposals under the assessment framework, not evidence that partnership or consultation occurred.

Proposed review gates; all open

| Gate | Proposed evidence before closure |
| --- | --- |
| CG01: language and names | Appropriate review of wording and alias display; AT09 supports only character preservation. |
| CG02: data approach | Agreed demonstration-data limits and any controls needed before real personal-data use. |
| CG03: participation and usability | Relevant user feedback on completing the workflow, barriers and agreed responses. |

The adviser may revise or replace these candidate gates. Record the actual date, appropriate role, permitted summary, resulting decision and follow-up only after contact. If access cannot be arranged, retain that status and the tutor’s guidance.

9. Collaboration and version-control evidence

Actual assistant baseline

A new local Git baseline was created during this revision by Codex Assistant. Commit: 38e8108564e6a34e04c74c9433ff89c41427b869. It records the reference code and reproducible checking tools. The associated metadata and restorable bundle are included in the ZIP.

This commit has its actual creation timestamp and an explicit assistant identity. It is one current baseline; it is not a history of student sprint work. Original application files remain unchanged. No member authorship, old commits, remote repository or peer approval is implied.

| Evidence file | Use |
| --- | --- |
| version_control/git_metadata.json | Commit/tree identity, author and time for the assistant baseline. |
| version_control/git_log.txt | Actual baseline history. |
| version_control/baseline.bundle | Recoverable Git repository snapshot. |
| verification/verification.json | Execution environment, technical results and source identities. |
| agile/product_backlog.md and sprint_backlog.md | Named roles, scope, estimated work and explicitly simulated progress. |

Communication and review model

The scenario selects Teams for messages and shared agendas, Markdown backlogs for task allocation, and Git for version control. Teams use and student collaboration are not evidenced. An existing team communication service may be used instead; the case does not require a new paid account.

Before a meeting, Xuerui shares the goal, questions and decisions needed. Members give completed work, next step and blocker updates. Yonghui records actions with owners and a target review. Bin links each demonstrated behaviour to its story. A written response route remains available after the discussion.

Definition of Done and honest tracking

A real task reaches Done only when its agreed behaviour is implemented, relevant checks pass, a second member reviews it and evidence is linked. Technical test passes, client acceptance and cultural review have separate statuses. The scenario backlog uses “complete in the case” and does not claim these student steps have occurred.

The assistant activity log in the ZIP records only this revision’s observable work: source comparison, verification and artifact preparation. The three members should use their own identities and current dates for subsequent work. Detailed steps for starting from the baseline are provided with the bundle.

10. Cost estimate and delivery risks

This is an effort and resource estimate for the classroom scenario. It assumes 18 hours per role at NZD 30 per hour, existing equipment and existing communication-tool access. The rate is a coursework assumption, not a market quotation or a payment record.

| Item | Calculation / assumption | NZD |
| --- | --- | --- |
| Xuerui Huang: labour | 18 h x 30 | 540 |
| Bin Wang: labour | 18 h x 30 | 540 |
| Yonghui Dai: labour | 18 h x 30 | 540 |
| Tools | Python/SQLite, Git, existing editor and assumed existing Teams access; no additional paid purchase. | 0 |
| Resources | Assumed share of existing computer/network use. | 30 |
| Subtotal | 1,620 + 0 + 30 | 1,650 |
| Contingency | 10% of subtotal | 165 |
| Total | 1,650 + 165 | 1,815 |

Basis, exclusions and changes

Sprint 1 contributes 23 hours and Sprint 2 contributes 31, totalling 54 hours. Each member has 18 estimated hours. A six-hour increase at the same rate adds NZD 180 before contingency, producing a revised total of NZD 2,013.

The estimate excludes tax, depreciation, hosting and any consultation fee. Agree consultation arrangements rather than assuming an adviser’s time is free. Add any new costs before contingency. No measured student timesheet or actual cost comparison is available.

Risks and responses

| Risk | Response / coordinator |
| --- | --- |
| Client arrangement unconfirmed | Xuerui checks the assessed client-role arrangement with the tutor; retains the internal scenario as preparation. |
| Advisory access unavailable | Yonghui requests a suitable route and records the actual response; cultural gates remain open. |
| Uneven understanding of the code | All members explain a successful and a rejected operation; cross-review responsibilities. |
| Demonstration fails on another machine | Bin keeps the baseline; Yonghui verifies the final extracted product on the presentation computer. |
| Real personal data used prematurely | Use fictional aliases; obtain an agreed data/control plan before real operation. |

No extra GUI, authentication or online booking is required for this defined prototype. A wider deployment would require a separate scope and estimate.

11. Actual technical execution and acceptance

Run date: 13 October 2026 (Pacific/Auckland). Executor: assistant. Environment: Python 3.12.14, Darwin arm64, SQLite 3.53.1. Tests use temporary databases and fictional values, leaving the user’s existing database untouched.

The nine original unit checks and ten acceptance-style checks passed during this revision. The reusable acceptance_checks.py is now included, so the team can repeat the workflow against its own final version.

| Check / story | Observed result | Status |
| --- | --- | --- |
| AT01 / US01 | Fresh database shows three available items and empty history. | PASS |
| AT02 / US02 | Loan 1 created, borrower recorded and laptop marked On loan. | PASS |
| AT03 / US02 | Duplicate borrow rejected without an additional record. | PASS |
| AT04 / US02 | Unknown ID, blank, spaces-only, 81-character and control-character aliases rejected. | PASS |
| AT05 / US03 | Return timestamp stored, laptop available and historical loan retained. | PASS |
| AT06 / US03 | Repeated and nonexistent returns rejected; record count unchanged. | PASS |
| AT07 / US04 | Empty, returned and active history states displayed correctly. | PASS |
| AT08 / US05 | A separate process preserves active loans and the three-item inventory. | PASS |
| AT09 / US06 | Māia preserved in storage and UTF-8 CLI output after restart; physical display not assessed. | PASS |
| AT10 / UI | Non-numeric ID and invalid menu choice rejected; subsequent inventory action works. | PASS |

Reproduce and demonstrate

Extract the product and open a terminal in Campus_Equipment_Loan_System. Run python3 -m unittest -v, then python3 acceptance_checks.py. Use python3 app.py --db rehearsal.db for the demonstration. On Windows, py may replace python3.

Demonstration sequence: list equipment; borrow device 1 with a fictional alias; attempt a duplicate; return the displayed loan ID; inspect history; restart with the same database; confirm the records remain. The automated checker also covers invalid IDs/aliases and macrons.

Acceptance status and limits

Technical checks: PASS. Client-role acceptance: simulated only. Cultural review: OPEN. A successful automated run cannot establish client satisfaction or Māori-specific suitability. Physical classroom display, fault recovery, performance, operational security and independent user acceptance are outside these results.

12. Evidence register and submission readiness

| Item | Evidence status | Supported conclusion |
| --- | --- | --- |
| Python application and tests | ACTUAL reference artifact | The documented local workflow is implemented. |
| Unit tests + AT01-AT10 | ACTUAL assistant execution | Observed behaviour for the source identified in the verification files. |
| Assistant Git baseline and bundle | ACTUAL current baseline | Versioned reference and reproducible starting point; no student history. |
| M01-M04, D01-D04, CF01-CF04 | SIMULATED case records | A complete example connecting needs, reviews and scope decisions. |
| Two sprints and 54 hours | SIMULATED plan and effort | Reasoned task allocation and cost estimate; no actual timesheet. |
| CG01-CG03 consultation material | PREPARED; review OPEN | Questions and candidate criteria; no adviser involvement. |
| Group and individual reflections | SIMULATED role-based analysis | Reasoning to review and adapt; not personal statements by the named students. |

What is complete in the package

The package contains a running prototype, specifications, six stories, two sprint backlogs, worked meeting and feedback records, an estimate, a consultation briefing, technical verification, a recoverable baseline and completed reflection examples. Editable records and a simulation-ready presentation script are included in the ZIP.

Remaining participation and administrative details

For an assessed account of real coursework, the team must carry out the required client-role and collaboration activities, obtain the appropriate consultation arrangement, and confirm each member’s contributions and reflection. These are participant actions rather than missing report prose. The scenario records remain useful preparation.

[TO COMPLETE: student IDs, tutor and submission date]

Authorship and references

AI assistance produced the reference implementation and drafted the scenario, reports and checking tools. Actual assistant activity is identified in the evidence. Describe the team’s subsequent work and follow the course’s assistance/disclosure requirements.

Source: Yoobee, MSE800 Professional Software Engineering, Assessment 2: Object-Oriented Project, supplied brief, pp. 1-7. The partnership, participation and protection framework used here follows that brief. Code and execution records in the product ZIP support implementation and test claims. Fictional activity records are not external sources.

13. Task-by-task requirement check

All eight assessment tasks require a response. The table distinguishes completed written material and technical evidence from student activity or consultation still to occur. It does not predict a grade.

| Task / weighting | Report coverage | Evidence boundary |
| --- | --- | --- |
| 1. Team formation / 10% | Sections 1-2; three roles and inclusive agreement. | Roles are assigned; student teamwork has not been evidenced. |
| 2. Kickoff / 10% | Section 5: M01 and D01-D04; section 8: cultural briefing. | Client-role needs are simulated; actual consultation is outstanding. |
| 3. Requirements meetings / 15% | Section 5: M02, questions, decisions and action owners. | Complete scenario record; no actual participant meeting record. |
| 4. Analysis / priorities / 10% | Section 3: stories, business value and local-impact assessment. | Written analysis complete; priorities require client-role confirmation. |
| 5. Agile sprints / 15% | Sections 6-7: 14 tasks and reviews; section 9: tools and actual Git baseline. | Current assistant version control exists; student iterations, messages and reviews are not evidenced. |
| 6. Cost estimate / 10% | Section 10: labour, tools, resources, assumptions and contingency. | Estimate complete at NZD 1,815; no actual expenditure is claimed. |
| 7. Acceptance / testing / 10% | Sections 3, 8 and 11: criteria for every story, executed checks, open cultural gates. | 9 + 10 technical checks passed; user/community acceptance and adviser-agreed criteria remain open. |
| 8. Reflection / 20% | Reflection Report: group synthesis and three named examples. | All four themes covered; members must confirm accounts against their own experience. |

Assessment scope

The submission format remains two PDFs and one runnable product ZIP; backlogs are within the ZIP. The brief also requires a final presentation of the product and development journey. It specifies no mandatory GUI, programming language, report word count or presentation duration.

The brief permits classroom simulation of developer/client roles. The team must confirm the assessed arrangement rather than treating this written persona as independent client participation. Tasks 2 and 7 explicitly request Kaiārahi consultation even though the scenario describes an external guide as something a team “could” have.

Ethnic-diversity information is omitted from completion fields at the team’s request. The original Task 1/rubric still includes it; no tutor waiver is claimed. Other cultural collaboration and Te Tiriti requirements remain. Task 1 partnership implementation and Task 4 community priorities have the applicability conditions stated in the brief.