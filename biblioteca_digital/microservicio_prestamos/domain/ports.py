from abc import ABC, abstractmethod
from typing import List, Optional
from .models.loan import Loan

class LoanRepositoryPort(ABC):
    """
    Define el contrato que cualquier adaptador de base de datos
    debe cumplir para gestionar la persistencia de los préstamos.
    """

    @abstractmethod
    def save(self, loan: Loan) -> Loan:
        """Guarda un nuevo préstamo o actualiza uno existente."""
        pass

    @abstractmethod
    def find_by_id(self, loan_id: int) -> Optional[Loan]:
        """Busca un préstamo por su ID."""
        pass

    @abstractmethod
    def find_active_by_user_id(self, user_id: int) -> List[Loan]:
        """Encuentra todos los préstamos activos de un usuario."""
        pass