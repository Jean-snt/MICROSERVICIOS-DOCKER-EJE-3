from datetime import datetime, timedelta
from typing import List, Optional
from dataclasses import dataclass
from enum import Enum

class LoanStatus(Enum):
    """Estados posibles de un préstamo"""
    ACTIVE = "active"
    RETURNED = "returned"
    OVERDUE = "overdue"

@dataclass
class User:
    """Entidad de Usuario del dominio"""
    id: int
    name: str
    email: str
    status: str
    
    @property
    def is_active(self) -> bool:
        return self.status == 'active'
    
    @property
    def is_suspended(self) -> bool:
        return self.status == 'suspended'

@dataclass
class Book:
    """Entidad de Libro del dominio"""
    id: int
    title: str
    author: str
    isbn: str
    status: str
    
    @property
    def is_available(self) -> bool:
        return self.status == 'available'
    
    @property
    def is_deleted(self) -> bool:
        return self.status == 'deleted'

@dataclass
class Loan:
    """Entidad de Préstamo del dominio"""
    id: Optional[int]
    user_id: int
    book_id: int
    start_date: datetime
    due_date: datetime
    return_date: Optional[datetime]
    status: LoanStatus
    
    @property
    def is_active(self) -> bool:
        return self.status == LoanStatus.ACTIVE
    
    @property
    def is_overdue(self) -> bool:
        if not self.is_active:
            return False
        return datetime.now() > self.due_date
    
    @property
    def days_until_due(self) -> int:
        if not self.is_active:
            return 0
        delta = self.due_date - datetime.now()
        return max(0, delta.days)

class LoanDomainService:
    """Servicio de dominio para lógica de negocio de préstamos"""
    
    MAX_ACTIVE_LOANS = 3
    LOAN_DURATION_DAYS = 15
    
    def __init__(self, user_repository, book_repository, loan_repository):
        self.user_repository = user_repository
        self.book_repository = book_repository
        self.loan_repository = loan_repository
    
    def can_user_borrow_book(self, user_id: int) -> tuple[bool, str]:
        """
        Verifica si un usuario puede pedir un préstamo
        Retorna: (puede_prestar, mensaje_error)
        """
        # Verificar que el usuario existe y está activo
        user = self.user_repository.get_by_id(user_id)
        if not user:
            return False, "Usuario no encontrado"
        
        if not user.is_active:
            return False, "Usuario no está activo"
        
        if user.is_suspended:
            return False, "Usuario está suspendido"
        
        # Verificar límite de préstamos activos
        active_loans = self.loan_repository.get_active_loans_by_user(user_id)
        if len(active_loans) >= self.MAX_ACTIVE_LOANS:
            return False, f"Usuario ha alcanzado el límite de {self.MAX_ACTIVE_LOANS} préstamos activos"
        
        return True, ""
    
    def can_book_be_borrowed(self, book_id: int) -> tuple[bool, str]:
        """
        Verifica si un libro puede ser prestado
        Retorna: (puede_prestarse, mensaje_error)
        """
        # Verificar que el libro existe y está disponible
        book = self.book_repository.get_by_id(book_id)
        if not book:
            return False, "Libro no encontrado"
        
        if book.is_deleted:
            return False, "Libro ha sido eliminado"
        
        if not book.is_available:
            return False, "Libro no está disponible"
        
        return True, ""
    
    def create_loan(self, user_id: int, book_id: int) -> Loan:
        """
        Crea un nuevo préstamo aplicando todas las reglas de negocio
        """
        # Validar usuario
        can_borrow, user_error = self.can_user_borrow_book(user_id)
        if not can_borrow:
            raise ValueError(f"Error de usuario: {user_error}")
        
        # Validar libro
        can_be_borrowed, book_error = self.can_book_be_borrowed(book_id)
        if not can_be_borrowed:
            raise ValueError(f"Error de libro: {book_error}")
        
        # Crear préstamo
        now = datetime.now()
        due_date = now + timedelta(days=self.LOAN_DURATION_DAYS)
        
        loan = Loan(
            id=None,
            user_id=user_id,
            book_id=book_id,
            start_date=now,
            due_date=due_date,
            return_date=None,
            status=LoanStatus.ACTIVE
        )
        
        return loan
    
    def return_loan(self, loan_id: int) -> Loan:
        """
        Devuelve un préstamo
        """
        loan = self.loan_repository.get_by_id(loan_id)
        if not loan:
            raise ValueError("Préstamo no encontrado")
        
        if not loan.is_active:
            raise ValueError("El préstamo ya ha sido devuelto")
        
        loan.return_date = datetime.now()
        loan.status = LoanStatus.RETURNED
        
        return loan
