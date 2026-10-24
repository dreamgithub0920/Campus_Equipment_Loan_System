CAMPUS EQUIPMENT LOAN SYSTEM
MSE800 Assessment 2

REQUIREMENTS
Python 3.10+ with sqlite3; the desktop interface also requires Tkinter and a
graphical desktop session. No third-party Python packages are required.
The GUI and command-line interface share the same SQLite database and rules.
Use a writable local folder. Internet and compilation are not needed to run.

RUN THE DESKTOP INTERFACE
1. Extract 02_Product.zip completely.
2. On macOS, open Start_GUI.command, or run: bash Start_GUI.command
   This launcher finds Python 3.10+ with Tkinter. The system Python on some
   Macs is too old. On this Mac it can use the existing Codex Python runtime.
3. On Windows, double-click Start_GUI.bat after extracting the whole ZIP.
   It checks Python 3.10+, Tkinter and SQLite, then opens the same GUI.
   Install a Python distribution with Tcl/Tk support if the check fails.
4. From a suitable Python installation: python3 gui.py
   For a separate rehearsal database: python3 gui.py --db rehearsal.db
   On Windows: py -3 gui.py

WINDOWS QUICK START
Extract the ZIP to a writable local folder, for example a folder in Documents.
Open Campus_Equipment_Loan_System and double-click Start_GUI.bat. Keep every
source file together; do not run the launcher from the ZIP preview window.
The launcher tries py -3, python and python3 and keeps errors visible.
Python is required; this is a source-code product, not a standalone EXE.

To choose a separate database from Command Prompt in the product folder:
Start_GUI.bat --db "rehearsal.db"
To check the desktop dependency: py -3 -m tkinter
To check the program: py -3 -m unittest -v
Then run: py -3 acceptance_checks.py

Window size and font appearance can vary with Windows display scaling. On a
shorter window the summary cards hide to leave room for the loan history;
enlarge the window to show them again. Tables have scrollbars and the window
can be resized or maximised.
The application and GUI interactions were executed on macOS. The Windows
launcher has been reviewed but not executed on a Windows machine; a Windows
borrowing/return/restart check is still needed before presenting on Windows.

Select a device in Equipment, enter a name/alias and a required phone contact,
then click Record loan. Use fictional details for coursework demonstrations.
On-loan equipment cannot be borrowed again. Select an active row in Loan
history and click Return selected loan; returned records remain visible.
Active only filters the history. Refresh reloads the current database state.
Close and reopen with the same database to keep the saved records.

If Python reports that tkinter is missing, use a Python distribution with Tk
support. A GUI session is required; the terminal interface remains available
on systems without Tk or a display. Keep gui.py beside the other source files.

RUN THE COMMAND-LINE INTERFACE
1. Extract 02_Product.zip completely.
2. Open a terminal in Campus_Equipment_Loan_System.
3. Run: python3 app.py --db rehearsal.db
4. Use menu options 1-4; option 0 exits. On Windows, py may replace python3.

Without --db the program creates equipment.db beside app.py. It seeds Laptop,
Camera, Projector, Tablet and Microphone and preserves loan/return records
after restart, including phone contacts. A relative
custom database path is relative to the terminal directory. Its parent must
exist and be writable. Use fictional aliases and a separate rehearsal database.

PHONE CONTACT AND EXISTING DATA
Each new loan requires a phone contact containing 7-15 digits, with a maximum
of 30 characters including formatting. Spaces, hyphens, parentheses and one
leading + are accepted. The format check does not verify that a number exists
or that it belongs to the borrower. Names/aliases and contacts are stored with
each loan, not in a separate customer account.

On reopening the program, existing equipment.db files are upgraded automatically:
add the phone column and seed Tablet (ID 4) and Microphone (ID 5), retaining all
existing loans, identifiers and timestamps. Earlier records without a phone show
Not recorded. The app never creates a made-up contact for those records.
No database is included in the ZIP; a fresh extraction creates a clean database.
Keep your existing equipment.db if you want to retain earlier local history.
Close the old app window before starting the updated program.

CHECK
python3 -m unittest -v
python3 acceptance_checks.py
GUI checks only: python3 -m unittest test_gui -v
Business/storage checks only: python3 -m unittest test_system -v
Optional new acceptance output: python3 acceptance_checks.py --output-dir checks
Checks use disposable temporary databases. The complete unittest suite includes
12 business/storage checks plus eight GUI checks (20 total). GUI checks create real Tk widgets;
they are skipped when Tkinter or a desktop display is unavailable. Skipped
GUI checks do not establish that the desktop interface works on that machine.

FILES
app.py                  Menu and entry point
gui.py                  Desktop interface and GUI entry point
Start_GUI.command       Double-click launcher for macOS
Start_GUI.bat           Double-click launcher for Windows
models.py               Equipment and Loan data classes
service.py              Borrowing and return rules
repository.py           SQLite schema and queries
test_system.py          Twelve business/storage/migration checks
test_gui.py             Eight GUI interaction, layout and persistence checks
acceptance_checks.py    Twelve technical acceptance checks
agile/product_backlog.md Editable product backlog
agile/sprint_backlog.md  Editable sprint backlog

INTEGRATED REPORT EVIDENCE
The Project Report contains the product backlog (section 3.1), activity records
(sections 5-7), sprint backlog (sections 6-7), Git record (section 9), acceptance
output (section 11), unit output (Appendix A) and run/retrieval steps (Appendix B).
Separate verification/, version_control/ and documents/ folders are unnecessary
for this reduced runnable package. The two editable backlogs remain here.

SOURCE VERSION
Repository: https://github.com/dreamgithub0920/Campus_Equipment_Loan_System
Default branch: main
Product source files are directly in the repository root. The current release
adds a desktop GUI, Windows/macOS launchers, Tablet and Microphone, required
phone contacts and legacy-database migration. The Project Report section 9
records the exact source commit used by the release verification.


RETRIEVE THE CURRENT PRODUCT
 git clone --branch main https://github.com/dreamgithub0920/Campus_Equipment_Loan_System.git
 cd Campus_Equipment_Loan_System
 python3 gui.py --db rehearsal.db
On Windows use Start_GUI.bat or: py -3 gui.py --db rehearsal.db
On macOS use Start_GUI.command or: bash Start_GUI.command --db rehearsal.db
For the pinned source used in the report, check out the source commit recorded
in section 9 before running. Public retrieval needs no GitHub sign-in.
The repository also includes the two PDF reports, product ZIP and presentation
script at the root. The ZIP contains only the runnable product and backlogs.

GUI DESIGN AND VERIFICATION
This is a standalone desktop application: the interface, business rules and
SQLite database run on the same computer. It does not connect to a server.
Different computers do not automatically share or synchronise their records.
Keep the database on a writable local drive, not a shared network drive.

LoanApp (gui.py) displays equipment, summary counts and loan history using
Tkinter/ttk. It delegates borrowing and returns to the existing LoanService and
EquipmentRepository. GUI and CLI default to equipment.db beside the source;
--db selects another database. The repository adds borrower_phone to older databases automatically. New loans
require a phone contact, and the inventory now contains five devices.

The 24 October 2026 local verification covers GUI selection,
borrowing, Unicode aliases, invalid aliases, duplicate protection after a stale
selection, return by loan ID, active filtering, small-window layout, five-device inventory,
required phone validation, legacy-schema migration and persistence after reopening.


LIMITATIONS:
Undeployed classroom prototype with fixed inventory; no login, access controls,
encryption, deletion/retention workflow or reservations. Use fictional aliases.
Technical checks do not establish client or cultural acceptance.
