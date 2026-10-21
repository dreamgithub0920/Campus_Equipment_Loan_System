import tempfile
import unittest
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
        self.assertEqual([i.name for i in items], ['Laptop', 'Camera', 'Projector'])
        self.assertTrue(all(i.available for i in items))

    def test_borrow_updates_availability_and_history(self):
        loan_id = self.service.borrow(1, ' Demo A ')
        self.assertFalse(self.repository.equipment()[0].available)
        self.assertEqual(self.repository.loans()[0].borrower, 'Demo A')
        self.assertEqual(self.repository.loans()[0].id, loan_id)

    def test_double_borrow_is_rejected(self):
        self.service.borrow(1, 'Demo A')
        with self.assertRaisesRegex(ValueError, 'already on loan'):
            self.service.borrow(1, 'Demo B')
        self.assertEqual(len(self.repository.loans()), 1)

    def test_return_keeps_history_and_allows_new_loan(self):
        loan_id = self.service.borrow(1, 'Demo A')
        self.service.return_loan(loan_id)
        self.assertTrue(self.repository.equipment()[0].available)
        self.assertIsNotNone(self.repository.loans()[0].returned_at)
        self.service.borrow(1, 'Demo B')
        self.assertEqual(len(self.repository.loans()), 2)

    def test_invalid_equipment_id(self):
        with self.assertRaisesRegex(ValueError, 'not found'):
            self.service.borrow(999, 'Demo A')
        self.assertEqual(self.repository.loans(), [])

    def test_invalid_alias(self):
        for alias in ['', '   ', 'x' * 81, 'Bad\nName']:
            with self.subTest(alias=repr(alias)):
                with self.assertRaises(ValueError):
                    self.service.borrow(1, alias)
        self.assertEqual(self.repository.loans(), [])

    def test_missing_or_repeated_return(self):
        with self.assertRaises(ValueError):
            self.service.return_loan(999)
        loan_id = self.service.borrow(1, 'Demo A')
        self.service.return_loan(loan_id)
        with self.assertRaises(ValueError):
            self.service.return_loan(loan_id)

    def test_unicode_alias_round_trip(self):
        self.service.borrow(1, 'Māia 示例')
        self.assertEqual(self.repository.loans()[0].borrower, 'Māia 示例')

    def test_persistence_after_restart(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'test.db'
            first = EquipmentRepository(path)
            try:
                LoanService(first).borrow(2, 'Demo C')
            finally:
                first.close()
            second = EquipmentRepository(path)
            try:
                self.assertFalse(second.equipment()[1].available)
                self.assertEqual(second.loans()[0].borrower, 'Demo C')
                self.assertEqual(len(second.equipment()), 3)
            finally:
                second.close()


if __name__ == '__main__':
    unittest.main()
