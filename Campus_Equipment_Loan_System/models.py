"""Small domain objects for the campus equipment prototype."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Equipment:
    id: int
    name: str
    available: bool


@dataclass(frozen=True)
class Loan:
    id: int
    equipment_name: str
    borrower: str
    borrowed_at: str
    returned_at: str | None
    borrower_phone: str = ""
