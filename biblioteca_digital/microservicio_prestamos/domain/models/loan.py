from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass
class Loan:
    """
    Representa la entidad de negocio 'Préstamo' de forma pura.
    No sabe nada sobre bases de datos o frameworks.
    """
    id: Optional[int]
    user_id: int
    book_id: int
    loan_date: date
    due_date: date
    status: str = "activo"