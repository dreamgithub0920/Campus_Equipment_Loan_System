CAMPUS EQUIPMENT LOAN SYSTEM
MSE800 Assessment 2

REQUIREMENTS
Python 3.10+ with the standard sqlite3 module; writable local folder and terminal.
No external packages, internet connection or compilation step is needed to run.

RUN
1. Extract 02_Product.zip completely.
2. Open a terminal in Campus_Equipment_Loan_System.
3. Run: python3 app.py --db rehearsal.db
4. Use menu options 1-4; option 0 exits. On Windows, py may replace python3.

Without --db the program creates equipment.db beside app.py. It seeds Laptop,
Camera and Projector and preserves loan/return records after restart. A relative
custom database path is relative to the terminal directory. Its parent must
exist and be writable. Use fictional aliases and a separate rehearsal database.

CHECK
python3 -m unittest -v
python3 acceptance_checks.py
Optional new acceptance output: python3 acceptance_checks.py --output-dir checks
Both checking scripts use disposable temporary databases.

FILES
app.py                  Menu and entry point
models.py               Equipment and Loan data classes
service.py              Borrowing and return rules
repository.py           SQLite schema and queries
test_system.py          Nine unit checks
acceptance_checks.py    Ten technical acceptance checks
agile/product_backlog.md Editable product backlog
agile/sprint_backlog.md  Editable sprint backlog

INTEGRATED REPORT EVIDENCE
The Project Report contains the product backlog (section 3.1), activity records
(sections 5-7), sprint backlog (sections 6-7), Git record (section 9), acceptance
output (section 11), unit output (Appendix A) and run/retrieval steps (Appendix B).
Separate verification/, version_control/ and documents/ folders are unnecessary
for this reduced runnable package. The two editable backlogs remain here.

SOURCE VERSION


LIMITATIONS
Undeployed classroom prototype with fixed inventory; no login, access controls,
encryption, deletion/retention workflow or reservations. Use fictional aliases.
Technical checks do not establish client or cultural acceptance.
