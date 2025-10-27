from typing import List, Optional
from domain.entities import Loan, User, Book
from domain.ports import UserRepositoryPort, BookRepositoryPort, LoanRepositoryPort
from domain.entities import LoanDomainService

class LoanUseCase:
    """Caso de uso para gestionar préstamos"""
    
    def __init__(self, 
                 user_repository: UserRepositoryPort,
                 book_repository: BookRepositoryPort,
                 loan_repository: LoanRepositoryPort):
        self.user_repository = user_repository
        self.book_repository = book_repository
        self.loan_repository = loan_repository
        self.domain_service = LoanDomainService(
            user_repository, book_repository, loan_repository
        )
    
    def create_loan(self, user_id: int, book_id: int) -> Loan:
        """
        Crea un nuevo préstamo aplicando todas las reglas de negocio
        """
        # Crear préstamo usando el servicio de dominio
        loan = self.domain_service.create_loan(user_id, book_id)
        
        # Marcar libro como prestado en el servicio externo
        if not self.book_repository.mark_as_loaned(book_id):
            raise Exception("No se pudo marcar el libro como prestado")
        
        # Guardar préstamo en la base de datos local
        saved_loan = self.loan_repository.save(loan)
        
        return saved_loan
    
    def return_loan(self, loan_id: int) -> Loan:
        """
        Devuelve un préstamo
        """
        # Devolver préstamo usando el servicio de dominio
        loan = self.domain_service.return_loan(loan_id)
        
        # Marcar libro como disponible en el servicio externo
        if not self.book_repository.mark_as_available(loan.book_id):
            raise Exception("No se pudo marcar el libro como disponible")
        
        # Guardar cambios en la base de datos local
        saved_loan = self.loan_repository.save(loan)
        
        return saved_loan
    
    def get_user_active_loans(self, user_id: int) -> List[Loan]:
        """
        Obtiene todos los préstamos activos de un usuario
        """
        return self.loan_repository.get_active_loans_by_user(user_id)
    
    def get_loan_by_id(self, loan_id: int) -> Optional[Loan]:
        """
        Obtiene un préstamo por su ID
        """
        return self.loan_repository.get_by_id(loan_id)
    
    def get_all_active_loans(self) -> List[Loan]:
        """
        Obtiene todos los préstamos activos
        """
        return self.loan_repository.get_all_active_loans()
    
    def check_user_can_borrow(self, user_id: int) -> tuple[bool, str]:
        """
        Verifica si un usuario puede pedir un préstamo
        """
        return self.domain_service.can_user_borrow_book(user_id)
    
    def check_book_availability(self, book_id: int) -> tuple[bool, str]:
        """
        Verifica si un libro está disponible para préstamo
        """
        return self.domain_service.can_book_be_borrowed(book_id)
