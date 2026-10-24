import tempfile
import unittest
import sqlite3
from pathlib import Path
from repository import EquipmentRepository
from service import LoanService


class LoanTests(unittest.TestCase):
    def setUp(self):
        self.repository = EquipmentRepository(':memory:')
        self.service = LoanService(self.repository)

    def tearDown(self):
        self.repository.close()

    def test_initial_inventory(self):
        items = self.repository.equipment()
        self.assertEqual([i.name for i in items], ['Laptop', 'Camera', 'Projector', 'Tablet', 'Microphone'])
        self.assertTrue(all(i.available for i in items))

    def test_borrow_updates_availability_and_history(self):
        loan_id = self.service.borrow(1, ' Demo A ', '0200000000')
        self.assertFalse(self.repository.equipment()[0].available)
        self.assertEqual(self.repository.loans()[0].borrower, 'Demo A')
        self.assertEqual(self.repository.loans()[0].id, loan_id)

    def test_double_borrow_is_rejected(self):
        self.service.borrow(1, 'Demo A', '0200000000')
        with self.assertRaisesRegex(ValueError, 'already on loan'):
            self.service.borrow(1, 'Demo B', '0200000000')
        self.assertEqual(len(self.repository.loans()), 1)

    def test_return_keeps_history_and_allows_new_loan(self):
        loan_id = self.service.borrow(1, 'Demo A', '0200000000')
        self.service.return_loan(loan_id)
        self.assertTrue(self.repository.equipment()[0].available)
        self.assertIsNotNone(self.repository.loans()[0].returned_at)
        self.service.borrow(1, 'Demo B', '0200000000')
        self.assertEqual(len(self.repository.loans()), 2)

    def test_invalid_equipment_id(self):
        with self.assertRaisesRegex(ValueError, 'not found'):
            self.service.borrow(999, 'Demo A', '0200000000')
        self.assertEqual(self.repository.loans(), [])

    def test_invalid_alias(self):
        for alias in ['', '   ', 'x' * 81, 'Bad\nName']:
            with self.subTest(alias=repr(alias)):
                with self.assertRaises(ValueError):
                    self.service.borrow(1, alias, '0200000000')
        self.assertEqual(self.repository.loans(), [])

    def test_missing_or_repeated_return(self):
        with self.assertRaises(ValueError):
            self.service.return_loan(999)
        loan_id = self.service.borrow(1, 'Demo A', '0200000000')
        self.service.return_loan(loan_id)
        with self.assertRaises(ValueError):
            self.service.return_loan(loan_id)

    def test_unicode_alias_round_trip(self):
        self.service.borrow(1, 'Māia 示例', '0200000000')
        self.assertEqual(self.repository.loans()[0].borrower, 'Māia 示例')

    def test_persistence_after_restart(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'test.db'
            first = EquipmentRepository(path)
            try:
                LoanService(first).borrow(2, 'Demo C', '0200000000')
            finally:
                first.close()
            second = EquipmentRepository(path)
            try:
                self.assertFalse(second.equipment()[1].available)
                self.assertEqual(second.loans()[0].borrower, 'Demo C')
                self.assertEqual(len(second.equipment()), 5)
                self.assertEqual(second.loans()[0].borrower_phone, '0200000000')
            finally:
                second.close()

    def test_phone_validation_and_format_preservation(self):
        for phone in ('', '   ', '123456', '1' * 16, 'call me', '+64abc1234567',
                      '123\n456789', '++64200000000', None, 200000000):
            with self.subTest(phone=phone):
                with self.assertRaisesRegex(ValueError, 'phone number'):
                    self.service.borrow(1, 'Demo', phone)
                self.assertEqual(self.repository.loans(), [])
        self.service.borrow(1, 'Demo', '  +64 (20) 000-0000  ')
        self.assertEqual(self.repository.loans()[0].borrower_phone, '+64 (20) 000-0000')

    def test_new_equipment_can_be_borrowed_and_returned(self):
        for identifier, name in [(4, 'Tablet'), (5, 'Microphone')]:
            loan_id = self.service.borrow(identifier, 'Demo', '0200000000')
            self.assertEqual(self.repository.loans()[-1].equipment_name, name)
            self.service.return_loan(loan_id)
        self.assertTrue(all(item.available for item in self.repository.equipment()))

    def test_legacy_database_is_upgraded_without_losing_loans(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'legacy.db'
            with sqlite3.connect(path) as old:
                old.executescript('''
                    CREATE TABLE equipment (id INTEGER PRIMARY KEY, name TEXT NOT NULL);
                    CREATE TABLE loans (id INTEGER PRIMARY KEY, equipment_id INTEGER NOT NULL,
                        borrower TEXT NOT NULL, borrowed_at TEXT NOT NULL,
                        returned_at TEXT);
                    INSERT INTO equipment VALUES (1, 'Laptop'), (2, 'Camera'), (3, 'Projector');
                    INSERT INTO loans VALUES (7, 2, 'Legacy demo', '2026-10-20 09:00:00', NULL);
                ''')
            for iteration in range(2):
                repository = EquipmentRepository(path)
                try:
                    loans = repository.loans()
                    self.assertEqual(len(repository.equipment()), 5)
                    self.assertEqual(len(loans), 1)
                    self.assertEqual(loans[0].id, 7)
                    self.assertEqual(loans[0].borrower, 'Legacy demo')
                    self.assertEqual(loans[0].borrowed_at, '2026-10-20 09:00:00')
                    self.assertEqual(loans[0].borrower_phone, '')
                    self.assertEqual(loans[0].returned_at, None if iteration == 0 else '2026-10-24 09:00:00')
                    if iteration == 0:
                        repository.connection.execute(
                            "UPDATE loans SET returned_at = '2026-10-24 09:00:00' WHERE id = 7")
                        repository.connection.commit()
                finally:
                    repository.close()


if __name__ == '__main__':
    unittest.main()
