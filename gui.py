"""Desktop interface. Run with Python 3.10+: python3 gui.py."""
import argparse
from pathlib import Path
import sqlite3
import sys
import tkinter as tk
from tkinter import messagebox, ttk

from repository import EquipmentRepository
from service import LoanService


class LoanApp(ttk.Frame):
    """Present inventory and loans while LoanService handles the rules."""

    def __init__(self, root, repository):
        super().__init__(root, padding=18, style="Page.TFrame")
        self.repository = repository
        self.service = LoanService(repository)
        self.alias = tk.StringVar()
        self.phone = tk.StringVar()
        self.selected_device = tk.StringVar(value="Select a device from the list")
        self.active_only = tk.BooleanVar(value=False)
        self.notice = tk.StringVar(value="Select an available device to start a loan.")
        root.title("Campus Equipment Loan System")
        width = min(1120, max(800, root.winfo_screenwidth() - 80))
        height = min(800, max(640, root.winfo_screenheight() - 100))
        root.geometry(f"{width}x{height}")
        root.minsize(min(980, width), 640)
        self._styles(root)
        self.pack(fill="both", expand=True)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(4, weight=1)
        self._build()
        self.summary_visible = True
        root.bind("<Configure>", self._resize, add="+")
        root.bind("<Control-r>", lambda event: self.refresh())
        if root.tk.call("tk", "windowingsystem") == "aqua":
            root.bind("<Command-r>", lambda event: self.refresh())
        self.refresh(announce=False)

    @staticmethod
    def _styles(root):
        style = ttk.Style(root)
        style.theme_use("clam")
        root.configure(background="#f3f5f9")
        style.configure(".", font=("Arial", 12), foreground="#20354b")
        style.configure("Page.TFrame", background="#f3f5f9")
        style.configure("Panel.TFrame", background="white")
        style.configure("Page.TLabel", background="#f3f5f9")
        style.configure("Title.TLabel", background="#f3f5f9", font=("Arial", 22, "bold"))
        style.configure("Panel.TLabel", background="white")
        style.configure("Section.TLabel", background="white", font=("Arial", 14, "bold"))
        style.configure("Muted.TLabel", background="white", foreground="#586b7c", font=("Arial", 11))
        style.configure("Number.TLabel", background="white", font=("Arial", 22, "bold"))
        style.configure("TButton", padding=(13, 7))
        style.configure("Primary.TButton", background="#156b70", foreground="white", borderwidth=0)
        style.map("Primary.TButton", background=[("disabled", "#e1e7eb"), ("active", "#10565a")],
                  foreground=[("disabled", "#687786")])
        style.configure("TEntry", padding=5)
        style.configure("TCheckbutton", background="white")
        style.configure("Treeview", rowheight=28, background="white", fieldbackground="white", borderwidth=0)
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"), padding=(8, 6), background="#eaf0f4")
        style.map("Treeview", background=[("selected", "#d8eaea")], foreground=[("selected", "#123d42")])
        style.configure("Notice.TLabel", background="#e7f0f4", padding=9, foreground="#20354b")
        style.configure("Success.TLabel", background="#e4f2eb", padding=9, foreground="#1c6143")
        style.configure("Error.TLabel", background="#fbe9e6", padding=9, foreground="#a03025")

    def _build(self):
        header = ttk.Frame(self, style="Page.TFrame")
        header.grid(row=0, column=0, sticky="ew", pady=(0, 14))
        ttk.Label(header, text="Campus equipment loans", style="Title.TLabel").pack(anchor="w")
        ttk.Label(header, text="View availability, record a loan and keep track of returns.",
                  style="Page.TLabel").pack(anchor="w", pady=(5, 0))

        summary = self.summary = ttk.Frame(self, style="Page.TFrame")
        summary.grid(row=1, column=0, sticky="ew", pady=(0, 14))
        self.counts = {}
        for index, title in enumerate(("Total equipment", "Available", "On loan")):
            summary.columnconfigure(index, weight=1, uniform="cards")
            card = ttk.Frame(summary, padding=(16, 9), style="Panel.TFrame")
            card.grid(row=0, column=index, sticky="ew", padx=(0 if index == 0 else 12, 0))
            ttk.Label(card, text=title, style="Muted.TLabel").pack(anchor="w")
            self.counts[title] = tk.StringVar(value="0")
            ttk.Label(card, textvariable=self.counts[title], style="Number.TLabel").pack(anchor="w", pady=(4, 0))

        top = ttk.Frame(self, style="Page.TFrame")
        top.grid(row=2, column=0, sticky="ew", pady=(0, 12))
        top.columnconfigure(0, weight=3)
        top.columnconfigure(1, weight=2)
        inventory_panel = ttk.Frame(top, padding=12, style="Panel.TFrame")
        inventory_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 16))
        ttk.Label(inventory_panel, text="Equipment", style="Section.TLabel").pack(anchor="w", pady=(0, 12))
        self.inventory = self._tree(inventory_panel, [
            ("id", "ID", 55), ("name", "Equipment", 170), ("status", "Status", 140)
        ], height=3)
        self.inventory.bind("<<TreeviewSelect>>", self._select_device)

        borrow_panel = ttk.Frame(top, padding=12, style="Panel.TFrame")
        borrow_panel.grid(row=0, column=1, sticky="nsew")
        ttk.Label(borrow_panel, text="New loan", style="Section.TLabel").pack(anchor="w")
        ttk.Label(borrow_panel, textvariable=self.selected_device, style="Muted.TLabel").pack(anchor="w", pady=(7, 8))
        fields = ttk.Frame(borrow_panel, style="Panel.TFrame")
        fields.pack(fill="x")
        for column in (0, 1):
            fields.columnconfigure(column, weight=1, uniform="borrow_fields")
        ttk.Label(fields, text="Name / alias *", style="Panel.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(fields, text="Phone number *", style="Panel.TLabel").grid(row=0, column=1, sticky="w", padx=(8, 0))
        self.alias_entry = ttk.Entry(fields, textvariable=self.alias, width=15)
        self.alias_entry.grid(row=1, column=0, sticky="ew", pady=(4, 6))
        self.phone_entry = ttk.Entry(fields, textvariable=self.phone, width=15)
        self.phone_entry.grid(row=1, column=1, sticky="ew", padx=(8, 0), pady=(4, 6))
        self.alias_entry.bind("<Return>", lambda event: self.phone_entry.focus_set())
        self.phone_entry.bind("<Return>", lambda event: self.borrow_equipment())
        self.borrow_button = ttk.Button(borrow_panel, text="Record loan", command=self.borrow_equipment,
                                        style="Primary.TButton", state="disabled")
        self.borrow_button.pack(fill="x")

        self.notice_label = ttk.Label(self, textvariable=self.notice, style="Notice.TLabel", wraplength=900)
        self.notice_label.grid(row=3, column=0, sticky="ew", pady=(0, 12))

        history_panel = ttk.Frame(self, padding=12, style="Panel.TFrame")
        history_panel.grid(row=4, column=0, sticky="nsew")
        history_panel.columnconfigure(0, weight=1)
        history_panel.rowconfigure(1, weight=1)
        toolbar = ttk.Frame(history_panel, style="Panel.TFrame")
        toolbar.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        ttk.Label(toolbar, text="Loan history", style="Section.TLabel").pack(side="left")
        self.return_button = ttk.Button(toolbar, text="Return selected loan", command=self.return_selected,
                                        state="disabled")
        self.return_button.pack(side="right")
        ttk.Checkbutton(toolbar, text="Active only", variable=self.active_only,
                        command=lambda: self.refresh(announce=False)).pack(side="right", padx=16)
        table_frame = ttk.Frame(history_panel, style="Panel.TFrame")
        table_frame.grid(row=1, column=0, sticky="nsew")
        self.history = self._tree(table_frame, [
            ("id", "Loan ID", 80), ("equipment", "Equipment", 115), ("alias", "Borrower alias", 140),
            ("phone", "Phone number", 150),
            ("borrowed", "Borrowed (UTC)", 165), ("returned", "Returned (UTC)", 165),
            ("status", "Status", 90)
        ], height=6)
        self.history.bind("<<TreeviewSelect>>", self._select_loan)
        self.history_hint = ttk.Label(history_panel, text="", style="Muted.TLabel")
        self.history_hint.grid(row=2, column=0, sticky="w", pady=(6, 0))

        footer = ttk.Frame(self, style="Page.TFrame")
        footer.grid(row=5, column=0, sticky="ew", pady=(10, 0))
        ttk.Label(footer, text="Use fictional details for demonstrations. Records are saved locally.", style="Page.TLabel").pack(side="left")
        ttk.Button(footer, text="Refresh", command=self.refresh).pack(side="right")

    @staticmethod
    def _tree(parent, columns, height):
        frame = ttk.Frame(parent, style="Panel.TFrame")
        frame.pack(fill="both", expand=True)
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)
        tree = ttk.Treeview(frame, columns=[c[0] for c in columns], show="headings",
                            selectmode="browse", height=height)
        for key, title, width in columns:
            tree.heading(key, text=title)
            tree.column(key, width=width, minwidth=50, stretch=key not in ("id", "status"), anchor="w")
        vertical = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        horizontal = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=vertical.set, xscrollcommand=horizontal.set)
        tree.grid(row=0, column=0, sticky="nsew")
        vertical.grid(row=0, column=1, sticky="ns")
        horizontal.grid(row=1, column=0, sticky="ew")
        tree.tag_configure("available", foreground="#22704c")
        tree.tag_configure("active", foreground="#8c5200")
        return tree

    def _message(self, text, kind="Notice"):
        self.notice.set(text)
        self.notice_label.configure(style=kind + ".TLabel")

    def _resize(self, event):
        if event.widget is not self.master:
            return
        # Preserve room for history rows on smaller laptop displays.
        show_summary = event.height >= 760
        if show_summary != self.summary_visible:
            self.summary_visible = show_summary
            if show_summary:
                self.summary.grid()
            else:
                self.summary.grid_remove()

    def _select_device(self, event=None):
        selected = self.inventory.selection()
        values = self.inventory.item(selected[0], "values") if selected else ()
        if values:
            self.selected_device.set(f"{values[1]} (ID {values[0]}) · {values[2]}")
        else:
            self.selected_device.set("Select a device from the list")
        enabled = bool(values) and values[2] == "Available"
        self.borrow_button.configure(state="normal" if enabled else "disabled")

    def _select_loan(self, event=None):
        selected = self.history.selection()
        values = self.history.item(selected[0], "values") if selected else ()
        enabled = bool(values) and values[-1] == "Active"
        self.return_button.configure(state="normal" if enabled else "disabled")

    @staticmethod
    def _replace_rows(tree, rows):
        selected = tree.selection()
        tree.delete(*tree.get_children())
        for identifier, values, tag in rows:
            tree.insert("", "end", iid=str(identifier), values=values, tags=(tag,))
        if selected and tree.exists(selected[0]):
            tree.selection_set(selected[0])

    def refresh(self, announce=True):
        try:
            equipment = self.repository.equipment()
            loans = self.repository.loans()
        except sqlite3.Error:
            self._message("Could not refresh the records. Check the database and try Refresh.", "Error")
            return False
        self._replace_rows(self.inventory, [
            (item.id, (item.id, item.name, "Available" if item.available else "On loan"),
             "available" if item.available else "active") for item in equipment
        ])
        shown = [loan for loan in reversed(loans) if not self.active_only.get() or loan.returned_at is None]
        self._replace_rows(self.history, [
            (loan.id, (loan.id, loan.equipment_name, loan.borrower, loan.borrower_phone or "Not recorded", loan.borrowed_at,
                       loan.returned_at or "—", "Active" if loan.returned_at is None else "Returned"),
             "active" if loan.returned_at is None else "available") for loan in shown
        ])
        available = sum(item.available for item in equipment)
        for key, value in [("Total equipment", len(equipment)), ("Available", available),
                           ("On loan", len(equipment) - available)]:
            self.counts[key].set(str(value))
        self.history_hint.configure(text=(f"{len(shown)} record(s) shown. Select an active loan to return it."
                                          if shown else "No active loans." if self.active_only.get() else "No loans yet."))
        self._select_device()
        self._select_loan()
        if announce:
            self._message("Equipment and loan history refreshed.")
        return True

    def borrow_equipment(self):
        selected = self.inventory.selection()
        if not selected:
            self._message("Select a device from the equipment list first.", "Error")
            return
        try:
            loan_id = self.service.borrow(int(selected[0]), self.alias.get(), self.phone.get())
        except ValueError as error:
            self._message(str(error), "Error")
            return
        except sqlite3.Error:
            self._message("Could not save the loan. Refresh the records before trying again.", "Error")
            return
        self.alias.set("")
        self.phone.set("")
        if self.refresh(announce=False):
            if self.history.exists(str(loan_id)):
                self.history.selection_set(str(loan_id))
                self.history.see(str(loan_id))
                self._select_loan()
            self._message(f"Loan {loan_id} recorded. The equipment is now on loan.", "Success")
        else:
            self._message(f"Loan {loan_id} was saved, but the display could not refresh. Use Refresh.", "Error")

    def return_selected(self):
        selected = self.history.selection()
        if not selected:
            self._message("Select an active loan from the history first.", "Error")
            return
        loan_id = int(selected[0])
        try:
            self.service.return_loan(loan_id)
        except ValueError as error:
            self._message(str(error), "Error")
            return
        except sqlite3.Error:
            self._message("Could not save the return. Refresh the records before trying again.", "Error")
            return
        if self.refresh(announce=False):
            self._message(f"Loan {loan_id} returned. The equipment is available again; its history is kept.", "Success")
        else:
            self._message(f"Loan {loan_id} was returned, but the display could not refresh. Use Refresh.", "Error")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", default=str(Path(__file__).with_name("equipment.db")),
                        help="SQLite database path; shared with app.py by default")
    args = parser.parse_args()
    try:
        root = tk.Tk()
    except tk.TclError as error:
        print(f"Cannot open the desktop interface: {error}", file=sys.stderr)
        return 1
    root.withdraw()
    try:
        repository = EquipmentRepository(args.db)
    except sqlite3.Error:
        messagebox.showerror("Cannot open database", "Choose an existing, writable folder for the database.", parent=root)
        root.destroy()
        return 1
    try:
        LoanApp(root, repository)
        root.deiconify()
        root.mainloop()
    finally:
        repository.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
