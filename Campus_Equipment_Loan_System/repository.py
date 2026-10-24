"""Persistence belongs here; the menu does not contain SQL."""
import sqlite3
from models import Equipment, Loan


class EquipmentRepository:
    def __init__(self, path):
        self.connection = sqlite3.connect(path)
        self.connection.execute('PRAGMA foreign_keys = ON')
        self.connection.executescript('''
            CREATE TABLE IF NOT EXISTS equipment (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS loans (
                id INTEGER PRIMARY KEY,
                equipment_id INTEGER NOT NULL REFERENCES equipment(id),
                borrower TEXT NOT NULL,
                borrower_phone TEXT NOT NULL DEFAULT '',
                borrowed_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                returned_at TEXT
            );
            CREATE UNIQUE INDEX IF NOT EXISTS one_active_loan
                ON loans(equipment_id) WHERE returned_at IS NULL;
        ''')
        with self.connection:
            columns = {row[1] for row in self.connection.execute('PRAGMA table_info(loans)')}
            if 'borrower_phone' not in columns:
                self.connection.execute(
                    "ALTER TABLE loans ADD COLUMN borrower_phone TEXT NOT NULL DEFAULT ''")
            self.connection.executemany(
                'INSERT OR IGNORE INTO equipment(id, name) VALUES (?, ?)',
                [(1, 'Laptop'), (2, 'Camera'), (3, 'Projector'),
                 (4, 'Tablet'), (5, 'Microphone')])

    def equipment(self):
        rows = self.connection.execute('''
            SELECT e.id, e.name, NOT EXISTS (
                SELECT 1 FROM loans l
                WHERE l.equipment_id = e.id AND l.returned_at IS NULL
            ) FROM equipment e ORDER BY e.id
        ''')
        return [Equipment(row[0], row[1], bool(row[2])) for row in rows]

    def create_loan(self, equipment_id, borrower, borrower_phone):
        with self.connection:
            cursor = self.connection.execute(
                'INSERT INTO loans(equipment_id, borrower, borrower_phone) VALUES (?, ?, ?)',
                (equipment_id, borrower, borrower_phone))
            return cursor.lastrowid

    def close_loan(self, loan_id):
        with self.connection:
            cursor = self.connection.execute('''
                UPDATE loans SET returned_at = CURRENT_TIMESTAMP
                WHERE id = ? AND returned_at IS NULL
            ''', (loan_id,))
            return cursor.rowcount == 1

    def loans(self):
        rows = self.connection.execute('''
            SELECT l.id, e.name, l.borrower, l.borrowed_at, l.returned_at, l.borrower_phone
            FROM loans l JOIN equipment e ON e.id = l.equipment_id
            ORDER BY l.id
        ''')
        return [Loan(*row) for row in rows]

    def close(self):
        self.connection.close()
