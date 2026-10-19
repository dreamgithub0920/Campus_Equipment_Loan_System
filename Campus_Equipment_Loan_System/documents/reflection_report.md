MSE800 / ASSESSMENT 2

Reflection Report

Classroom scenario and role-based analysis

Xuerui Huang, Bin Wang and Yonghui Dai

SIMULATED REFLECTION EXAMPLES. The group discussion and first-person passages analyse the written case. They are not statements supplied by the named students or records of their participation. The actual assistant checks and baseline do not establish individual learning or contribution.

Engineering choices

The classroom scenario keeps the product small enough to explain and test. M01 defines one operator, three fixed devices and fictional borrower aliases. Separating the menu, loan service and repository gives each role a clear responsibility. The service checks a request, while the database enforces the active-loan constraint. Preserving returned records makes the history useful. These choices support the borrowing workflow, although the prototype still lacks access controls and recovery procedures for a damaged database.

Teamwork and scope

M02 introduces a useful discussion about equipment IDs and loan IDs. The proposed M03 review checks that the displayed loan ID is used for returns, demonstrates duplicate rejection and confirms that history remains available. These are review points for existing behaviour, not evidence of defects repaired by the students. In M04, the reservation request is deferred because dates, booking conflicts and accounts would widen the scope. Keeping that decision in the backlog makes the tradeoff visible.

Cultural considerations and Te Tiriti

The main cultural challenge is knowing whose input is missing. A team-written consultation exercise supplies questions but cannot supply Māori advice. Under the assessment's framework, partnership requires appropriate input into decisions; participation requires opportunities to influence them. Protection includes examining data use and cultural representation. Fictional aliases and Unicode preservation support limited technical choices. They do not establish community acceptance. Actual guidance, its agreed use and any resulting changes remain to be recorded.

Improving the next iteration

The proposed role allocation can help coordination, but equal estimated hours cannot establish effective teamwork. A useful next review would have each member explain another component and record one unresolved question. The team should then connect actual feedback, changes and tests to the current Git version. Assistant checks and baseline commits must remain distinguishable from student contributions.

Xuerui Huang

Requirements, coordination and interface

SIMULATED ROLE EXAMPLE. Review the reasoning and replace case events with your own contribution before using it as a personal account.

Technical learning

In the classroom scenario, my role covers requirements and the terminal interface. M01 gives the project a manageable boundary: one operator and three fixed devices. I would translate each need into a user story with a result that can be observed. For borrowing, that means checking both successful recording and rejection of an unavailable device. A general statement such as 'manage equipment' leaves too much open to interpretation.

Evaluating requirements and teamwork

The equipment-ID and loan-ID discussion in M02 is the most useful example for this role. A user needs to know which number to enter, even when the service logic is correct. M03 therefore proposes checking the existing prompts and demonstrating a return with the displayed loan ID. It does not establish that a code defect was found or repaired. I would ask Bin to review that path and Yonghui to connect it to an acceptance check. Written follow-up would let members raise questions after the meeting.

Cultural considerations and Te Tiriti

The role also needs to recognise the limits of internally written requirements. Partnership would mean seeking appropriate guidance before treating cultural decisions as settled. Participation would require relevant people to influence the scope and wording, with a way to contribute beyond a live discussion. Protection would include questioning what borrower information is necessary. Preserving macrons is useful, but it cannot establish Māori acceptance. No adviser has contributed to this case, so I would keep that gap visible and ask the tutor about the appropriate route.

A specific next action

My proposed improvement is an observed usability check with the classroom client role. I would give the operator a borrowing-and-return task without explaining which ID to choose, then record completion, incorrect entries and questions. That record would show whether the wording needs revision and give the next requirements discussion a specific starting point.

Bin Wang

Domain model, business rules and integration

SIMULATED ROLE EXAMPLE. Review the reasoning and replace case events with your own contribution before using it as a personal account.

Technical learning

In the classroom scenario, my role concerns the domain objects and loan rules. LoanService receives an EquipmentRepository object, so composition connects the logic to storage without mixing it into the menu. Equipment and Loan describe the information passed between components. This design is sufficient for the fixed inventory; a hierarchy of device subclasses would add work without answering an identified requirement.

Evaluating rules and scope

The duplicate-borrowing case makes the separation of responsibilities easier to explain. Service validation gives the operator a readable rejection, and the database constraint prevents a second active loan for the same item. A useful test also checks that no extra record appears. In the M03 review, I would demonstrate this path alongside a successful loan and return. The M04 reservation request should remain deferred until dates, booking conflicts and account requirements are understood. It cannot be treated as a small menu addition.

Teamwork and cultural considerations

Integration would benefit from a review with Xuerui that follows one request from the prompt through the service and repository. Yonghui could then check the stored result. That arrangement distributes understanding as well as tasks, although its effectiveness still needs to be observed. Te Tiriti also affects which requirements the team can decide alone. Partnership calls for appropriate guidance, and participation means leaving room for that input to change the design. Protection includes considering how data is handled. Unicode support addresses character preservation; it cannot establish whether Māori users find the interface appropriate. The consultation exercise contains no adviser endorsement.

A specific next action

My next action would be a recorded review of duplicate borrowing with another member. We would identify the service check and database constraint, run the rejection case and confirm that the loan count remains unchanged. The review note would name the tested version and record any part either person could not explain.

Yonghui Dai

Persistence, testing and evidence

SIMULATED ROLE EXAMPLE. Review the reasoning and replace case events with your own contribution before using it as a personal account.

Technical learning

In the classroom scenario, my role covers SQLite storage and testing. Persistence needs a check across separate program runs. Seeing a value immediately after borrowing does not prove that it will survive a restart. The test should reopen the same database and compare the loan history and equipment availability. Returned loans should remain visible, and restarting should not duplicate the three seeded devices.

Evaluating test evidence

I would connect each acceptance criterion to an observed result and distinguish a checklist from an executed test. The M03 review proposes checking retained history, the correct loan ID and duplicate rejection. Invalid requests also need a record-count check because an error message alone does not prove that storage was unchanged. Any separately reported assistant tests support the reference version; they do not show that I ran them. The same boundary applies to an assistant-created Git baseline and later student contributions.

Teamwork, culture and Te Tiriti

Evidence recording can help the team avoid disagreements about what was decided. I would circulate a short meeting record for correction and link each action to its owner. For cultural questions, the record also needs to identify who supplied the guidance and how it may be used. Partnership requires appropriate involvement; participation requires an opportunity to influence the criteria. Protection includes careful handling of information and cultural material. The example uses fictional aliases and preserves Māia, but these choices do not demonstrate Māori acceptance. No actual consultation or approval can be inferred from the prepared questions.

A specific next action

My next action would be a restart test on the presentation computer using a freshly extracted ZIP and a separate demonstration database. I would record the commands, environment and observed history before and after reopening the program, then ask Bin to check the result against the persistence criterion. Any display or storage failure would remain an open issue.