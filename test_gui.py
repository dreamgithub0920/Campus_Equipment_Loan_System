"""Real Tk widget checks. Skipped when Tk or a desktop display is unavailable."""
from pathlib import Path
import tempfile
import unittest

try:
    import tkinter as tk
except ImportError:
    tk = None

from repository import EquipmentRepository
from service import LoanService


@unittest.skipIf(tk is None, "Tkinter is not installed")
class GuiTests(unittest.TestCase):
    def setUp(self):
        try:
            self.root = tk.Tk()
        except tk.TclError as error:
            self.skipTest(f"Desktop display unavailable: {error}")
        self.root.withdraw()
        self.addCleanup(self.root.destroy)
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.path = Path(self.directory.name) / "gui_test.db"
        self.repository = EquipmentRepository(self.path)
        self.addCleanup(self.repository.close)
        from gui import LoanApp
        self.app = LoanApp(self.root, self.repository)
        self.root.update()

    def select_device(self, identifier):
        self.app.inventory.selection_set(str(identifier))
        self.root.update()

    def borrow(self, identifier=1, alias="Māia", phone="0200000000"):
        self.select_device(identifier)
        self.app.alias.set(alias)
        self.app.phone.set(phone)
        self.app.borrow_button.invoke()
        self.root.update()

    def test_inventory_and_empty_history(self):
        self.assertEqual(self.app.inventory.get_children(), ("1", "2", "3", "4", "5"))
        self.assertEqual(self.app.counts["Available"].get(), "5")
        self.assertEqual(self.app.history.get_children(), ())
        self.assertTrue(self.app.return_button.instate(["disabled"]))

    def test_small_window_keeps_history_and_actions_visible(self):
        self.root.geometry("980x650")
        self.root.deiconify()
        self.root.update()
        self.assertFalse(self.app.summary.winfo_ismapped())
        self.assertGreaterEqual(self.app.history.winfo_height(), 100)
        for widget in (self.app.borrow_button, self.app.return_button, self.app.history_hint):
            self.assertTrue(widget.winfo_ismapped())
            self.assertLessEqual(widget.winfo_rooty() + widget.winfo_height(),
                                 self.root.winfo_rooty() + self.root.winfo_height())
        self.root.geometry("1120x800")
        self.root.update()
        self.assertTrue(self.app.summary.winfo_ismapped())

    def test_borrow_button_updates_tables_and_unicode(self):
        self.borrow(2)
        self.assertEqual(self.app.inventory.set("2", "status"), "On loan")
        self.assertEqual(self.app.history.set("1", "alias"), "Māia")
        self.assertEqual(self.app.history.set("1", "phone"), "0200000000")
        self.assertEqual(self.app.counts["On loan"].get(), "1")
        self.assertTrue(self.app.borrow_button.instate(["disabled"]))
        self.assertEqual(self.app.alias.get(), "")
        self.assertEqual(self.app.phone.get(), "")
        self.assertIn("Loan 1 recorded", self.app.notice.get())

    def test_return_uses_loan_id_and_keeps_history(self):
        self.borrow(3)
        self.app.return_button.invoke()
        self.root.update()
        self.assertEqual(self.app.inventory.set("3", "status"), "Available")
        self.assertEqual(self.app.history.set("1", "status"), "Returned")
        self.assertTrue(self.app.return_button.instate(["disabled"]))
        self.assertEqual(len(self.repository.loans()), 1)
        self.app.return_selected()
        self.assertIn("Active loan not found", self.app.notice.get())

    def test_alias_validation_and_missing_selection(self):
        self.app.borrow_equipment()
        self.assertIn("Select a device", self.app.notice.get())
        for alias in ("", "   ", "x" * 81, "bad\nname"):
            with self.subTest(alias=alias):
                self.borrow(alias=alias)
                self.assertIn("1 to 80 printable", self.app.notice.get())
                self.assertEqual(self.repository.loans(), [])

    def test_stale_inventory_rejects_duplicate(self):
        self.select_device(1)
        LoanService(self.repository).borrow(1, "Other operator", '0200000000')
        self.app.alias.set("Demo")
        self.app.phone.set("0200000000")
        self.app.borrow_button.invoke()
        self.assertIn("already on loan", self.app.notice.get())
        self.assertEqual(len(self.repository.loans()), 1)
        self.app.refresh()
        self.assertEqual(self.app.inventory.set("1", "status"), "On loan")

    def test_active_filter_and_restart_persistence(self):
        self.borrow()
        self.app.active_only.set(True)
        self.app.refresh(announce=False)
        self.app.return_button.invoke()
        self.assertEqual(self.app.history.get_children(), ())
        self.app.active_only.set(False)
        self.app.refresh(announce=False)
        self.assertEqual(self.app.history.set("1", "status"), "Returned")
        from gui import LoanApp
        self.app.destroy()
        self.repository.close()
        self.repository = EquipmentRepository(self.path)
        self.addCleanup(self.repository.close)
        reopened = LoanApp(self.root, self.repository)
        self.assertEqual(reopened.history.set("1", "alias"), "Māia")
        self.assertEqual(reopened.history.set("1", "status"), "Returned")
        self.assertEqual(reopened.history.set("1", "phone"), "0200000000")
        self.assertEqual(reopened.counts["Available"].get(), "5")

    def test_phone_is_required_and_new_equipment_can_be_selected(self):
        for phone in ('', 'bad phone', '123456', '1' * 16):
            self.borrow(4, phone=phone)
            self.assertIn('phone number', self.app.notice.get())
            self.assertEqual(self.repository.loans(), [])
        self.borrow(4, phone='+64 20 000 0000')
        self.assertEqual(self.app.history.set('1', 'equipment'), 'Tablet')
        self.assertEqual(self.app.history.set('1', 'phone'), '+64 20 000 0000')
        self.app.return_button.invoke()
        self.borrow(5)
        self.assertEqual(self.app.history.set('2', 'equipment'), 'Microphone')


if __name__ == "__main__":
    unittest.main()
