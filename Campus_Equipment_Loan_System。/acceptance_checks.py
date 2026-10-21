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
SOURCE_FILES = ("app.py", "models.py", "repository.py", "service.py", "test_system.py")


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
                    ("Laptop", "Camera", "Projector")), "Seed inventory is incorrect")
        rows.append(["AT01", "PASS", "Fresh database shows three available items and empty history."])

        borrowed = cli("AT02 borrow", "2\n1\nDemo A\n1\n4\n0\n")
        require("Loan ID: 1" in borrowed and "Laptop | On loan" in borrowed and
                "Demo A" in borrowed, "Borrowed item or displayed history is incorrect")
        rows.append(["AT02", "PASS", "Loan 1 created, borrower recorded and laptop marked On loan."])

        repository = EquipmentRepository(database)
        try:
            service = LoanService(repository)
            duplicate = cli("AT03 duplicate borrow", "2\n1\nDemo B\n0\n")
            require("already on loan" in duplicate and len(repository.loans()) == 1,
                    "Duplicate borrowing changed stored history")
            rows.append(["AT03", "PASS", "Duplicate borrow rejected without an additional record."])

            for item, alias in ((999, "Demo"), (2, ""), (2, "   "),
                                (2, "x" * 81), (2, "bad\nname")):
                try:
                    service.borrow(item, alias)
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

            active = cli("AT07 mixed history", "2\n2\nDemo C\n4\n0\n")
            require("Returned " in active and "Active" in active and
                    "Camera | Demo C" in active, "Active and returned history missing")
            rows.append(["AT07", "PASS", "Empty, returned and active history states displayed correctly."])

            restarted = cli("AT08 restart persistence", "1\n4\n0\n")
            require("Camera | On loan" in restarted and "Demo C" in restarted and
                    len(repository.equipment()) == 3, "Restart did not preserve state")
            rows.append(["AT08", "PASS", "A separate process preserves active loans and the three-item inventory."])

            cli("AT09 Unicode borrow", "2\n3\nMāia\n0\n")
            unicode_history = cli("AT09 Unicode restart", "4\n0\n")
            require("Māia" in unicode_history and repository.loans()[-1].borrower == "Māia",
                    "Unicode borrower alias changed")
            rows.append(["AT09", "PASS", "Māia preserved in storage and UTF-8 CLI output after restart; physical display not assessed."])

            recovered = cli("AT10 invalid input recovery", "2\nabc\n9\n1\n0\n")
            require("Input error:" in recovered and "Choose 0, 1, 2, 3, or 4." in recovered and
                    "Laptop | Available" in recovered, "Menu did not recover after invalid input")
            rows.append(["AT10", "PASS", "Non-numeric ID and invalid menu choice rejected; subsequent inventory action works."])
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
    print("\n10 technical acceptance checks passed; disposable database removed.")
    print("These results do not record student participation, client sign-off or cultural approval.")


if __name__ == "__main__":
    main()
