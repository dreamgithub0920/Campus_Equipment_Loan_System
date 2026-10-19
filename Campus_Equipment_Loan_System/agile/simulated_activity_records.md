# Simulated client-role and development records

SIMULATION ONLY. This is the written case, not observed student activity. No customer or adviser has endorsed these records. Relative days are illustrative, not calendar dates.

## Kickoff and requirements

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

## Sprint 1 review

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

## Sprint 2 review

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