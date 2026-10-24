"""Business rules are independent of the command-line interface."""
import sqlite3
import re


class LoanService:
    def __init__(self, repository):
        self.repository = repository

    def borrow(self, equipment_id, borrower, borrower_phone=""):
        borrower = borrower.strip()
        if not borrower or len(borrower) > 80 or not borrower.isprintable():
            raise ValueError('Use a borrower alias of 1 to 80 printable characters.')
        phone_error = ('Enter a phone number with 7-15 digits. Spaces, hyphens, '
                       'parentheses and a leading + are allowed.')
        if not isinstance(borrower_phone, str):
            raise ValueError(phone_error)
        borrower_phone = borrower_phone.strip()
        if (len(borrower_phone) > 30 or
                re.fullmatch(r'\+?[0-9 ()-]+', borrower_phone) is None or
                not 7 <= sum(char.isdigit() for char in borrower_phone) <= 15):
            raise ValueError(phone_error)
        item = next((item for item in self.repository.equipment()
                     if item.id == equipment_id), None)
        if item is None:
            raise ValueError('Equipment ID not found.')
        if not item.available:
            raise ValueError('This equipment is already on loan.')
        try:
            return self.repository.create_loan(equipment_id, borrower, borrower_phone)
        except sqlite3.IntegrityError as error:
            raise ValueError('Equipment is unavailable. Refresh the equipment list.') from error

    def return_loan(self, loan_id):
        if not self.repository.close_loan(loan_id):
            raise ValueError('Active loan not found. Check the loan ID.')
