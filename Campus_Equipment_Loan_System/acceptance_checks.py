"""Portable technical acceptance checks; run: python3 acceptance_checks.py.

Uses only the Python standard library and a disposable temporary database.
This checks software behaviour, not client acceptance or cultural endorsement.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import sqlite3
import subprocess
import sys
import tempfile

from repository import EquipmentRepository
from service import LoanService


CODE = Path(__file__).resolve().parent
SOURCE_FILES = ("app.py", "gui.py", "models.py", "repository.py", "service.py",
                "test_system.py", "test_gui.py", "acceptance_checks.py")


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def run_checks():
    rows = []
    transcripts = []
    with tempfile.TemporaryDirectory(prefix="mse800_acceptance_") as directory:
        database = Path(directory) / "acceptance.db"

        def cli(label, input_text):
            environment = dict(os.environ, PYTHONIOENCODING="utf-8")
            result = subprocess.run(
                [sys.executable, str(CODE / "app.py"), "--db", str(database)],
                input=input_text, text=True, encoding="utf-8", capture_output=True,
                timeout=15, check=True, env=environment,
            )
            transcripts.append(
                "CASE: " + label + "\nINPUT:\n" + input_text +
                "OUTPUT:\n" + result.stdout + "STDERR:\n" + result.stderr
            )
            return result.stdout

        fresh = cli("AT01 fresh inventory and empty history", "4\n1\n0\n")
        require("No loans yet." in fresh, "Fresh history must be empty")
        require(all(name + " | Available" in fresh for name in
                    ("Laptop", "Camera", "Projector", "Tablet", "Microphone")), "Seed inventory is incorrect")
        rows.append(["AT01", "PASS", "Fresh database shows five available items and empty history."])

        borrowed = cli("AT02 borrow", "2\n1\nDemo A\n0200000000\n1\n4\n0\n")
        require("Loan ID: 1" in borrowed and "Laptop | On loan" in borrowed and
                "Demo A" in borrowed and "Phone: 0200000000" in borrowed,
                "Borrowed item or displayed history is incorrect")
        rows.append(["AT02", "PASS", "Loan 1 created with borrower and phone; laptop marked On loan."])

        repository = EquipmentRepository(database)
        try:
            service = LoanService(repository)
            duplicate = cli("AT03 duplicate borrow", "2\n1\nDemo B\n0200000000\n0\n")
            require("already on loan" in duplicate and len(repository.loans()) == 1,
                    "Duplicate borrowing changed stored history")
            rows.append(["AT03", "PASS", "Duplicate borrow rejected without an additional record."])

            for item, alias in ((999, "Demo"), (2, ""), (2, "   "),
                                (2, "x" * 81), (2, "bad\nname")):
                try:
                    service.borrow(item, alias, '0200000000')
                except ValueError:
                    pass
                else:
                    raise AssertionError("Invalid ID or alias was accepted: " + repr((item, alias)))
            require(len(repository.loans()) == 1, "Rejected inputs changed stored history")
            rows.append(["AT04", "PASS", "Unknown ID, blank, spaces-only, 81-character and control-character aliases rejected."])

            returned = cli("AT05 return", "3\n1\n1\n4\n0\n")
            require("Returned successfully." in returned and "Laptop | Available" in returned,
                    "Return did not update the interface")
            require(repository.loans()[0].returned_at is not None,
                    "Return timestamp was not persisted")
            rows.append(["AT05", "PASS", "Return timestamp stored, laptop available and historical loan retained."])

            repeated = cli("AT06 invalid returns", "3\n1\n3\n999\n0\n")
            require(repeated.count("Active loan not found") == 2 and
                    len(repository.loans()) == 1, "Invalid returns changed stored history")
            rows.append(["AT06", "PASS", "Repeated and nonexistent returns rejected; record count unchanged."])

            active = cli("AT07 mixed history", "2\n2\nDemo C\n0200000000\n4\n0\n")
            require("Returned " in active and "Active" in active and
                    "Camera | Demo C" in active, "Active and returned history missing")
            rows.append(["AT07", "PASS", "Empty, returned and active history states displayed correctly."])

            restarted = cli("AT08 restart persistence", "1\n4\n0\n")
            require("Camera | On loan" in restarted and "Demo C" in restarted and
                    len(repository.equipment()) == 5 and "Phone: 0200000000" in restarted,
                    "Restart did not preserve state")
            rows.append(["AT08", "PASS", "A separate process preserves loans, phone contacts and the five-item inventory."])

            cli("AT09 Unicode borrow", "2\n3\nMāia\n0200000000\n0\n")
            unicode_history = cli("AT09 Unicode restart", "4\n0\n")
            require("Māia" in unicode_history and repository.loans()[-1].borrower == "Māia",
                    "Unicode borrower alias changed")
            rows.append(["AT09", "PASS", "Māia preserved in storage and UTF-8 CLI output after restart; physical display not assessed."])

            recovered = cli("AT10 invalid input recovery", "2\nabc\n9\n1\n0\n")
            require("Input error:" in recovered and "Choose 0, 1, 2, 3, or 4." in recovered and
                    "Laptop | Available" in recovered, "Menu did not recover after invalid input")
            rows.append(["AT10", "PASS", "Non-numeric ID and invalid menu choice rejected; subsequent inventory action works."])

            for identifier, name in ((4, "Tablet"), (5, "Microphone")):
                new_loan = cli("AT11 borrow " + name,
                               f"2\n{identifier}\nDemo equipment\n0200000000\n0\n")
                require("Borrowed successfully" in new_loan, name + " could not be borrowed")
                loan_id = repository.loans()[-1].id
                returned_new = cli("AT11 return " + name, f"3\n{loan_id}\n0\n")
                require("Returned successfully" in returned_new and
                        repository.loans()[-1].returned_at is not None,
                        name + " could not be returned")
            rows.append(["AT11", "PASS", "Tablet and Microphone can each be borrowed and returned using their loan IDs."])

            before_count = len(repository.loans())
            for phone in ("", "123456", "x1234567", "1" * 16, "++64200000000"):
                rejected = cli("AT12 invalid phone", f"2\n1\nDemo phone\n{phone}\n0\n")
                require("Enter a phone number" in rejected and len(repository.loans()) == before_count,
                        "Invalid phone was saved")
            cli("AT12 formatted phone", "2\n1\nDemo phone\n+64 (20) 000-0000\n0\n")
            phone_history = cli("AT12 phone after restart", "4\n0\n")
            require("Phone: +64 (20) 000-0000" in phone_history and
                    repository.loans()[-1].borrower_phone == "+64 (20) 000-0000",
                    "Formatted phone was not preserved")
            rows.append(["AT12", "PASS", "Missing/invalid phone contacts rejected; a formatted contact persists after restart."])
        finally:
            repository.close()
    return rows, "\n\n".join(transcripts)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path,
                        help="Optional directory for JSON and CLI transcript; no files otherwise")
    args = parser.parse_args()
    checks, transcript = run_checks()
    result = {
        "executed_at_utc": datetime.now(timezone.utc).isoformat(),
        "scope": "Technical verification only; not client acceptance or cultural endorsement",
        "python": platform.python_version(),
        "platform": platform.system() + " " + platform.machine(),
        "sqlite": sqlite3.sqlite_version,
        "checks": checks,
        "source_sha256": {name: hashlib.sha256((CODE / name).read_bytes()).hexdigest()
                          for name in SOURCE_FILES},
    }
    if args.output_dir:
        args.output_dir.mkdir(parents=True, exist_ok=True)
        (args.output_dir / "acceptance_results.json").write_text(
            json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (args.output_dir / "cli_transcript.txt").write_text(transcript, encoding="utf-8")
    for identifier, status, detail in checks:
        print(identifier + " " + status + ": " + detail)
    print(f"\n{len(checks)} technical acceptance checks passed; disposable database removed.")
    print("These results do not record student participation, client sign-off or cultural approval.")


if __name__ == "__main__":
    main()
