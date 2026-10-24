# Three-person presentation: current desktop product and classroom case

Members: Xuerui Huang, Bin Wang, Yonghui Dai.

Updated 24 October 2026. The script distinguishes the current working product,
assistant-run checks and written classroom case. The proposed first-person role
analysis is not evidence of individual student contribution. Review it against
actual experience before assessment. Timing is a rehearsal suggestion.

| Part | Topic | Speaker | Suggested time |
| --- | --- | --- | --- |
| 1 | Scope, current requirements and roles | Xuerui Huang | 90 seconds |
| 2 | Baseline sprints, later requests and revised cost | Xuerui Huang | 90 seconds |
| 3 | Object-oriented design | Bin Wang | 60 seconds |
| 4 | Live GUI demonstration | Bin Wang | 2 minutes |
| 5 | Tests, migration and Git source | Yonghui Dai | 90 seconds |
| 6 | Culture, Te Tiriti and next review | Yonghui Dai | 90 seconds |

## Xuerui Huang: scope, requirements and coordination

Good morning. We are Xuerui Huang, Bin Wang and Yonghui Dai. Our project is the
Campus Equipment Loan System, a local desktop application built with Python and
SQLite. It manages a laptop, camera, projector, tablet and microphone.

The operator can check availability, record borrowing with a name or alias and
phone number, register a return and review the saved history. The GUI and terminal
interface use the same rules and database. It works on one computer without a
server; records do not automatically synchronise between computers.

The six user stories cover availability, borrowing, return, history, persistence
and Unicode names. A new loan needs a phone contact containing seven to fifteen
digits. Spaces, hyphens, parentheses and one leading plus are allowed. This is a
format check, not proof that the number exists. Demonstrations use fictional details.

Our proposed roles remain requirements/interface coordination for me, domain rules
and integration for Bin, and persistence/testing/evidence for Yonghui. The two
written baseline sprints total 54 estimated hours. They are classroom examples,
not completed student meeting records. The later owner requests add the GUI,
Windows launcher, two devices and required phone contact; they are recorded separately.

The revised planning model adds twelve hours, suggested as four per member for
adaptation and review. That makes 66 hours at 30 New Zealand dollars per hour.
With 30 dollars for resources and ten-percent contingency, the current estimate
is 2,211 dollars. It is not a timesheet or a record of payments.

I will now hand over to Bin for the design and demonstration.

## Bin Wang: design and GUI demonstration

The application separates presentation, business rules and storage. LoanApp in
gui.py displays the desktop interface, while app.py keeps the terminal workflow.
Both call LoanService. The service receives an EquipmentRepository object,
which stores and retrieves records in SQLite. Equipment and Loan are data classes.

LoanService validates the alias and phone and rejects unavailable devices. The
database also has an index that prevents two active loans for the same device.
Tablet and Microphone use the existing equipment model; no extra subclass is needed.

I will use a separate demonstration database. First, I show the inventory and
scroll to Tablet and Microphone. I select Tablet, enter Demo A and a fictional
phone, then click Record loan. A new Loan ID appears in history, together with
the saved phone, and the tablet becomes On loan.

The Record loan button is disabled for that on-loan device. The service also
rejects duplicate requests if another operation has changed the data. I select
the active history row and click Return selected loan. The tablet becomes
available again and the returned record stays visible.

Next I select Microphone and leave the phone empty. The program rejects the
request without adding a record. I enter a valid fictional contact and record
the loan. I then close and reopen with the same database: the contact and history
remain. A later loan ID can differ from the equipment ID, so returns use the loan row.

Online booking remains deferred because it introduces dates, conflicts and access
decisions. This release stays a small standalone desktop product. I will hand
over to Yonghui for verification and reflection.

## Yonghui Dai: tests, migration, culture and reflection

The current assistant-run verification on 24 October passed twelve business and
storage checks, eight GUI checks and twelve acceptance checks. The GUI checks
create real Tk widgets and cover selection, input validation, return, filtering,
restart and a smaller window. These results describe software observations;
they do not establish that the named students ran the checks or that a client approved it.

Older databases are upgraded automatically by adding borrower_phone. Existing
loan identifiers and timestamps are kept. A contact that was never collected
stays blank and displays Not recorded. Migration checks compare old and new
records instead of inventing missing information.

The public GitHub repository is dreamgithub0920/Campus_Equipment_Loan_System.
The main branch contains the current release. The pinned product source is
d61c66ca11d2fd69c2bd40c005d3e4b53f65b100. The report records its actual author and timestamp. A later
documentation commit contains the reports, product ZIP and this presentation
script. The current source was matched to the package; earlier history is preserved.

The Mac application was executed and the Windows launcher was reviewed. A real
Windows borrowing/return/restart check is still needed on the presentation computer.
Tkinter or a desktop display may be absent, so skipped GUI checks do not prove
that the interface works on a machine.

The phone requirement also changes the cultural and data discussion. Partnership
means seeking appropriate guidance, participation means allowing relevant people
to influence the requirement, and protection includes examining why contacts are
collected and how they are kept. The prototype stores details locally without
login or encryption, so demonstrations use fictional data. Unicode support,
including macrons, cannot establish cultural acceptance.

No actual Kaiārahi consultation or community approval is claimed. The next steps
are a presentation-machine check, the tutor's client and advisory arrangement,
cross-review of the code and personal reflections based on actual contributions.
Thank you.

## Demonstration checklist

1. Extract the current ZIP completely. Use a fresh demonstration database:
   macOS: `bash Start_GUI.command --db presentation_demo.db`.
   Windows: `Start_GUI.bat --db presentation_demo.db`.
   If that filename already holds a rehearsal, choose another filename.
2. Show equipment and scroll to Tablet (4) and Microphone (5).
3. Select Tablet, enter `Demo A` and fictional phone `0200000000`, then Record loan.
4. Show the phone and Loan ID in history and the disabled borrow button for an on-loan device.
5. Select the active loan and Return selected loan; confirm retained history.
6. Select Microphone, omit the phone and show the rejection; supply a fictional contact and retry.
7. Close and reopen using the same command/database; show that the history and phone remain.
8. Explain that legacy records without a phone show Not recorded. Do not reset an existing database.
9. If asked, run `python3 -m unittest -v` and `python3 acceptance_checks.py`;
   on Windows use `py -3` instead of `python3`.

Review personal statements against actual participation. The proposed classroom
meetings and consultation cannot be presented as having occurred during this demo.
