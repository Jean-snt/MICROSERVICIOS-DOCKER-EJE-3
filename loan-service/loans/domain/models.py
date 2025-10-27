"""
loan_microservice/loans/domain/models.py

Define la entidad principal (Loan) del dominio. Esta clase es el corazón de la
lógica de negocio y es independiente de la base de datos o el framework.
"""
from datetime import date, timedelta
from typing import Optional
from .exceptions import LoanMaxDurationExceededError

class Loan:
    """
    Entidad de Dominio para un Préstamo de Libro Digital.
    Contiene la lógica y el estado del préstamo.
    """
    MAX_DURATION_DAYS = 15 # Requisito de negocio 3.2: Duración máxima

    def __init__(self,
                 user_id: str,
                 book_id: str,
                 start_date: date,
                 due_date: date,
                 id: Optional[str] = None,
                 return_date: Optional[date] = None):
        """
        Inicializa una instancia de Préstamo.

        Args:
            user_id (str): ID del usuario que solicita el préstamo.
            book_id (str): ID del libro prestado.
            start_date (date): Fecha de inicio del préstamo.
            due_date (date): Fecha de vencimiento del préstamo.
            id (Optional[str]): ID único del préstamo (puede ser generado por el adaptador de persistencia).
            return_date (Optional[date]): Fecha de devolución del libro (si ya fue devuelto).
        """
        self.id = id
        self.user_id = user_id
        self.book_id = book_id
        self.start_date = start_date
        self.due_date = due_date
        self.return_date = return_date

    def is_active(self) -> bool:
        """Verifica si el préstamo está activo (no ha sido devuelto)."""
        return self.return_date is None

    def is_overdue(self) -> bool:
        """Verifica si el préstamo ha vencido y aún está activo."""
        return self.is_active() and date.today() > self.due_date

    def mark_as_returned(self) -> None:
        """Marca el préstamo como devuelto en la fecha actual."""
        if self.is_active():
            self.return_date = date.today()

    @classmethod
    def create_new(cls, user_id: str, book_id: str, duration_days: int) -> 'Loan':
        """
        Método de fábrica para crear un nuevo préstamo, aplicando la regla de duración máxima.

        Args:
            user_id (str): ID del usuario.
            book_id (str): ID del libro.
            duration_days (int): Duración solicitada del préstamo en días.

        Returns:
            Loan: Nueva instancia de préstamo.

        Raises:
            LoanMaxDurationExceededError: Si la duración excede el máximo.
        """
        if duration_days > cls.MAX_DURATION_DAYS:
            raise LoanMaxDurationExceededError(max_days=cls.MAX_DURATION_DAYS)

        start_date = date.today()
        due_date = start_date + timedelta(days=duration_days)

        # El ID se establecerá al ser guardado por el adaptador de persistencia
        return cls(
            user_id=user_id,
            book_id=book_id,
            start_date=start_date,
            due_date=due_date
        )
    
    def to_dict(self) -> dict:
        """Convierte la entidad en un diccionario para uso en adaptadores (ej. JSON/DB)."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'book_id': self.book_id,
            'start_date': self.start_date.isoformat(),
            'due_date': self.due_date.isoformat(),
            'return_date': self.return_date.isoformat() if self.return_date else None,
            'is_active': self.is_active(),
            'is_overdue': self.is_overdue(),
        }
