"""
loan_microservice/loans/application/services.py

Define los Casos de Uso (Application Services) que orquestan el flujo de negocio.
Esta capa SÓLO interactúa con las Entidades del Dominio y las interfaces de Puertos.
"""
from typing import Optional, List
from datetime import date
from ..domain.entities import LoanEntity
from ..domain.exceptions import (
    MaxActiveLoansReachedError, 
    UserSuspendedError, 
    BookUnavailableError,
    LoanNotFoundError,
)
from ..domain.ports import LoanRepositoryPort, UserServicePort, BookServicePort

class LoanService:
    """
    Servicio de Aplicación para la gestión de préstamos.
    Implementa el flujo principal y aplica las reglas de negocio, usando los puertos.
    """

    def __init__(self, 
                 repository: LoanRepositoryPort, 
                 user_port: UserServicePort, 
                 book_port: BookServicePort):
        """
        Inicializa el servicio inyectando los puertos requeridos.
        Esta es la Inversión de Dependencias en acción.
        """
        self.repository = repository
        self.user_port = user_port
        self.book_port = book_port
        self.MAX_LOANS = 3 # Regla de negocio 3.2

    def create_loan(self, user_id: str, book_id: str, duration_days: int) -> LoanEntity:
        """
        Flujo Principal de Préstamos:
        1. Valida estado de Usuario y límite.
        2. Valida disponibilidad del Libro.
        3. Crea y persiste el Préstamo.
        4. Actualiza el estado del Libro.
        """
        # 1. Validar estado de Usuario y límite (Reglas 3.2)
        user = self.user_port.get_user(user_id)
        if not user or not user.can_request_loan()[0]:
            # El puerto debe lanzar UserSuspendedError o una excepción similar si falla
            raise UserSuspendedError(user_id) 

        active_loans = self.repository.find_active_by_user(user_id)
        active_loans_count = len(active_loans)
        if active_loans_count >= self.MAX_LOANS:
            raise MaxActiveLoansReachedError(user_id, self.MAX_LOANS)

        # 2. Validar disponibilidad del Libro (Regla 3.2)
        book = self.book_port.get_book(book_id)
        if not book or not book.can_be_loaned()[0]:
            # El puerto debe lanzar BookUnavailableError si falla
            raise BookUnavailableError(book_id, "no está disponible para préstamo")

        # 3. Crear y persistir el Préstamo (Lógica de Dominio)
        # El método create_new_loan en la entidad LoanEntity valida la duración máxima (15 días)
        new_loan = LoanEntity.create_new_loan(user_id, book_id)
        saved_loan = self.repository.save(new_loan)

        # 4. Actualizar estado del Libro
        self.book_port.mark_book_as_loaned(book_id)

        return saved_loan

    def return_loan(self, loan_id: str) -> LoanEntity:
        """
        Proceso para marcar un préstamo como devuelto.
        """
        loan = self.repository.find_by_id(loan_id)
        
        if loan is None:
            raise LoanNotFoundError(loan_id)

        # Lógica de Dominio: marca como devuelto
        loan.mark_as_returned()
        
        # Persistencia
        updated_loan = self.repository.save(loan)

        # Notificar al microservicio de Libros que el libro vuelve a estar disponible
        self.book_port.mark_book_as_available(loan.book_id)

        return updated_loan
    
    # Podríamos añadir más métodos (ej: get_loan, get_all_loans) si son necesarios para el negocio.
    
