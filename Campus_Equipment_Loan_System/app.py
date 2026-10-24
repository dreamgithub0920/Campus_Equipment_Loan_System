"""Run with Python 3.10 or later: python3 app.py"""
import argparse
from pathlib import Path
import sqlite3
from repository import EquipmentRepository
from service import LoanService


def run(repository):
    service = LoanService(repository)
    print('Campus Equipment Loan System - classroom prototype')
    print('Use fictional borrower details for demonstrations. Records are stored locally.')
    while True:
        print('\n1. View equipment\n2. Borrow equipment\n3. Return equipment'
              '\n4. View loan history\n0. Exit')
        choice = input('Choose: ').strip()
        try:
            if choice == '0':
                return
            if choice == '1':
                for item in repository.equipment():
                    status = 'Available' if item.available else 'On loan'
                    print(f'{item.id} | {item.name} | {status}')
            elif choice == '2':
                equipment_id = int(input('Equipment ID: '))
                borrower = input('Fictional borrower alias: ')
                phone = input('Borrower phone number: ')
                loan_id = service.borrow(equipment_id, borrower, phone)
                print(f'Borrowed successfully. Loan ID: {loan_id}')
            elif choice == '3':
                loan_id = int(input('Loan ID: '))
                service.return_loan(loan_id)
                print('Returned successfully.')
            elif choice == '4':
                history = repository.loans()
                if not history:
                    print('No loans yet.')
                for loan in history:
                    state = f'Returned {loan.returned_at}' if loan.returned_at else 'Active'
                    print(f'{loan.id} | {loan.equipment_name} | {loan.borrower}'
                          f' | Phone: {loan.borrower_phone or "Not recorded"}'
                          f' | Borrowed {loan.borrowed_at} | {state} (UTC)')
            else:
                print('Choose 0, 1, 2, 3, or 4.')
        except ValueError as error:
            print(f'Input error: {error}')
        except sqlite3.Error as error:
            print(f'Database error: {error}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--db', default=str(Path(__file__).with_name('equipment.db')))
    args = parser.parse_args()
    repository = EquipmentRepository(args.db)
    try:
        run(repository)
    except (EOFError, KeyboardInterrupt):
        print('\nGoodbye.')
    finally:
        repository.close()


if __name__ == '__main__':
    main()
