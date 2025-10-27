"""
CAPA DE DOMINIO - ENTIDADES
Entidades de negocio puras, independientes de frameworks
"""
from dataclasses import dataclass
from datetime import date, timedelta
from typing import Optional


@dataclass
class LoanEntity:
    """
    Entidad de Dominio para Préstamo
    Contiene la lógica de negocio pura sin dependencias externas
    """
    user_id: int
    book_id: int
    start_date: date
    due_date: date
    status: str = 'active'
    id: Optional[int] = None
    return_date: Optional[date] = None
    
    # Constantes de reglas de negocio
    MAX_LOAN_DAYS = 15
    
    @classmethod
    def create_new_loan(cls, user_id: int, book_id: int) -> 'LoanEntity':
        """
        Factory method para crear un nuevo préstamo
        Aplica reglas de negocio para fechas
        """
        start_date = date.today()
        due_date = start_date + timedelta(days=cls.MAX_LOAN_DAYS)
        
        return cls(
            user_id=user_id,
            book_id=book_id,
            start_date=start_date,
            due_date=due_date,
            status='active'
        )
    
    def is_overdue(self) -> bool:
        """Verifica si el préstamo está vencido"""
        return self.status == 'active' and date.today() > self.due_date
    
    def mark_as_returned(self) -> None:
        """Marca el préstamo como devuelto"""
        self.return_date = date.today()
        self.status = 'returned'
    
    def validate(self) -> tuple[bool, str]:
        """
        Valida la entidad según reglas de negocio
        Returns: (es_valido, mensaje_error)
        """
        if self.user_id <= 0:
            return False, "ID de usuario inválido"
        
        if self.book_id <= 0:
            return False, "ID de libro inválido"
        
        if self.due_date < self.start_date:
            return False, "La fecha de vencimiento no puede ser anterior a la fecha de inicio"
        
        return True, ""


@dataclass
class UserEntity:
    """
    Entidad de Dominio para Usuario
    Representa los datos del usuario relevantes para préstamos
    """
    id: int
    email: str
    is_active: bool
    is_suspended: bool = False
    
    def can_request_loan(self) -> tuple[bool, str]:
        """
        Verifica si el usuario puede solicitar un préstamo
        Returns: (puede_solicitar, mensaje_error)
        """
        if not self.is_active:
            return False, "Usuario inactivo"
        
        if self.is_suspended:
            return False, "Usuario suspendido no puede solicitar préstamos"
        
        return True, ""


@dataclass
class BookEntity:
    """
    Entidad de Dominio para Libro
    Representa los datos del libro relevantes para préstamos
    """
    id: int
    title: str
    is_available: bool
    is_deleted: bool = False
    
    def can_be_loaned(self) -> tuple[bool, str]:
        """
        Verifica si el libro puede ser prestado
        Returns: (puede_prestarse, mensaje_error)
        """
        if self.is_deleted:
            return False, "Libro eliminado no disponible"
        
        if not self.is_available:
            return False, "Libro no disponible para préstamo"
        
        return True, ""



