CAMPUS EQUIPMENT LOAN SYSTEM
MSE800 Assessment 2 - classroom prototype

REQUIREMENTS
Python 3.10 or later, including its standard sqlite3 module.
No external packages, server, internet connection or compilation step is needed.

RUN
1. Extract the ZIP completely.
2. Open a terminal inside Campus_Equipment_Loan_System.
3. Run: python3 app.py
   Windows alternative: py app.py
4. Use menu options 1-4; use 0 to exit.

The program creates equipment.db beside app.py, with a laptop, camera and
projector. Reopening the program preserves borrowing and return records.
Use fictional aliases only. To keep a separate demonstration database:
    python3 app.py --db demo.db
A relative custom database path is resolved from the terminal working directory.
Its parent directory must exist and be writable.

VERIFY
Nine unit tests:
    python3 -m unittest -v
Ten technical acceptance checks against a disposable temporary database:
    python3 acceptance_checks.py
Optional acceptance JSON and CLI transcript:
    python3 acceptance_checks.py --output-dir acceptance-output
On Windows, replace python3 with py.
Tests use temporary databases and do not read or change an existing equipment.db.
Acceptance checks exit with an error if an expected behaviour is absent.
They cover inventory, borrowing, validation, return, history, restart, Unicode
storage and recovery after invalid input. They do not establish client sign-off,
actual student participation, cultural approval or physical display quality.

FILES
app.py                  CLI menu and entry point
models.py               Equipment and Loan data classes
service.py              Borrowing and return business rules
repository.py           SQLite storage and queries
test_system.py          Nine automated unit tests
acceptance_checks.py    Ten portable technical acceptance checks
.gitignore              Excludes local databases and Python cache files
agile/                  Clearly labelled worked case records and workflow
verification/           Assistant-run technical evidence, with dates and scope
version_control/        Assistant baseline bundle and restoration instructions

SOURCE AND VERSION CONTROL
The initial reference implementation was prepared with AI assistance. Its five
original Python source files are preserved byte-for-byte in this package.
A portable acceptance script and an explicit local assistant baseline were
added on 13 October 2026 (Pacific/Auckland). The baseline author is
Codex Assistant <codex-assistant@example.invalid>. This is one actual current
commit, not student authorship or reconstructed historical sprint commits.
The baseline contains the runnable source, tests and run instructions. The
accompanying reports, scenario records and test evidence are outside that commit.
Read version_control/RESTORE.txt to inspect or restore the supplied Git bundle.
Students should review and understand the reference, disclose assistance as the
course requires, and record only their own later work under their own identity.
Git is optional for running this product; it is a development process tool.

LIMITATIONS
This is an undeployed local classroom prototype with fixed sample inventory.
There is no login, access control, encryption or online deployment.
Anyone with local database access can read stored records. Do not use real
personal data for the classroom demonstration. No existing database is supplied.

SCENARIO AND EVIDENCE STATUS
The agile materials are explicitly labelled simulated examples. Their meetings,
role-play feedback and sprint decisions must not be read as observed student
activities, real client approval or Maori/Kaiarahi advice. Current technical
verification and the assistant baseline are real recorded assistant actions.
