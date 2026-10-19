# Three-person presentation: classroom simulation and verified prototype

Members: Xuerui Huang, Bin Wang, Yonghui Dai.

This script is complete for explaining the written scenario and verified reference product. It does not assert that the students held the example meetings or that a Kaiārahi provided advice. Use it as a case-study rehearsal; personal contribution claims need to reflect the team's actual subsequent work. The timing below is a rehearsal suggestion, not an assessment rule.

| Slide | Topic | Speaker | Suggested time |
| --- | --- | --- | --- |
| 1 | Project and evidence status | Xuerui Huang | 30 seconds |
| 2 | Requirements, client role and priorities | Xuerui Huang | 60 seconds |
| 3 | Team roles, sprints and cost | Xuerui Huang | 60 seconds |
| 4 | Object-oriented design | Bin Wang | 60 seconds |
| 5 | Live demonstration | Bin Wang; Yonghui operates if useful | 2 minutes |
| 6 | Tests and Git baseline | Yonghui Dai | 60 seconds |
| 7 | Cultural preparation and Te Tiriti | Yonghui Dai | 60 seconds |
| 8 | Reflection and next steps | All, closing by Yonghui | 60 seconds |

## Xuerui Huang: project, requirements and coordination

Good morning. We are Xuerui Huang, Bin Wang and Yonghui Dai. Our project is the Campus Equipment Loan System.

We are presenting a classroom case study and a working reference prototype. The meeting and sprint records are illustrative. The software, recorded assistant-run checks and assistant Git baseline are real. The case does not claim completed student meetings or external cultural approval.

The client persona is an equipment desk operator who manages a laptop, camera and projector. The operator needs to know which item is available, record a loan and later register its return. We use fictional borrower aliases for demonstration.

The case has six user stories: view equipment, borrow, return, view history, preserve records after restart and preserve Unicode aliases. Borrowing and returning are the core workflow. Persistence prevents records from being lost, while history allows earlier loans to be checked. Online reservations, accounts and payments are outside the scope.

The proposed roles are simple. I cover requirements, coordination, the menu and report integration. Bin covers the domain model, business rules and integration. Yonghui covers storage, tests and evidence. Everyone also has a review and presentation role.

The case uses two short sprints. The first covers the inventory and borrowing workflow, including storage and alias handling. The second reviews return, history and persistence and prepares acceptance testing. A review question connects the two sprints: equipment ID and loan ID have different meanings. The demonstration needs to make that difference clear.

The estimate is 1,815 New Zealand dollars. It includes 54 hours at 30 dollars per hour, 30 dollars for resources and a ten-percent contingency. These are planning assumptions, not recorded payments or measured student hours.

My main lesson from analysing the case is that a requirement needs an observable result. For example, a duplicate loan should be rejected without adding another record. I will now hand over to Bin for the design and demonstration.

## Bin Wang: design and demonstration

Thank you. The prototype uses Python and SQLite, with a terminal menu.

The design separates the menu, business rules and storage. Equipment and Loan are data classes. LoanService checks borrowing and return rules. EquipmentRepository stores and retrieves the data. The menu calls the service instead of containing SQL.

The service receives a repository object. This is composition, and it makes the rules easier to test separately from interactive input. The database also has a constraint that prevents two active loans for one item. The service gives a readable error message, and the constraint protects the stored data.

I will demonstrate the workflow with a separate database and fictional aliases. First, the list shows the available devices. I select the laptop and enter Demo A. The program reports a new loan ID and marks the laptop as on loan.

If I try to borrow the laptop again, the program rejects the request. I then return the item using the displayed loan ID. The laptop becomes available, and the returned record stays in the history.

Finally, I exit and reopen the program with the same database. The history remains. A second borrowing cycle may produce a loan ID different from the equipment ID, which is why the operator should use the displayed number for returns.

In the written client-review example, online booking is requested but deferred. It would introduce dates, booking conflicts and further access decisions. My design lesson is to explain these consequences before treating a new request as a small menu change.

I will now hand over to Yonghui for testing and cultural considerations.

## Yonghui Dai: tests, cultural preparation and reflection

Thank you. Each user story has an acceptance criterion. The recorded assistant execution passed nine unit tests and ten additional technical acceptance checks on 13 October 2026. The acceptance script is included so the checks can be repeated.

The checks cover inventory, borrowing, duplicate rejection, invalid input, return, history, restart and Unicode preservation. They use disposable databases. The results verify software behaviour; they are not evidence that the three students personally ran those checks or that a client accepted the product.

A current Git baseline is also included. Its author is clearly identified as the assistant, and it can be restored from a bundle. It gives us a versioned starting point. Future student work should be recorded under the person who actually performs it.

For cultural preparation, the report follows the assessment's partnership, participation and protection framework. Partnership means seeking appropriate input before cultural decisions are settled. Participation means giving relevant people a meaningful opportunity to influence requirements. Protection includes asking what information and cultural material should be used and how it should be handled.

The prototype preserves macrons in fictional aliases, such as Māia. It does not collect contact details or ethnicity. These features support limited technical choices, but they do not prove cultural suitability. No Kaiārahi has been consulted for this written case. The prepared briefing asks about appropriate participants, wording, data handling, barriers and acceptance criteria. Those review gates remain open.

My main lesson is to distinguish an expected result from an observed result, and a technical result from someone's approval. The next team steps are to review the program together, test on the presentation computer, follow the tutor's client and consultation arrangements, and update the reflections with actual contributions. Thank you.

## Demonstration notes

1. Before presenting, open the final extracted product folder and use a new, writable demonstration database path: `python3 app.py --db presentation_demo.db`. If that file already contains a rehearsal, choose a new filename rather than assuming it is empty.
2. Option 1: show inventory.
3. Option 2: borrow device 1 with `Demo A`; note the displayed loan ID.
4. Option 2 again: device 1 with `Demo B`; show duplicate rejection.
5. Option 3: return the actual displayed loan ID.
6. Option 4: show the returned history.
7. Option 0: exit. Run the same command and show history again.
8. If time allows, borrow again and point out that the loan ID can differ from equipment ID.

On Windows, `py` may replace `python3`. Do not claim that a proposed classroom review or cultural consultation occurred during the technical demonstration.
