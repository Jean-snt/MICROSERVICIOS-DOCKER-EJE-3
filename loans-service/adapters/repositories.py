from django.db import models
from typing import List, Optional
from domain.entities import User, Book, Loan, LoanStatus
from domain.ports import UserRepositoryPort, BookRepositoryPort, LoanRepositoryPort
from .external_services import ExternalUserServiceAdapter, ExternalBookServiceAdapter

class UserRepositoryAdapter(UserRepositoryPort):
    """Adaptador del repositorio de usuarios usando servicios externos"""
    
    def __init__(self):
        self.external_service = ExternalUserServiceAdapter()
    
    def get_by_id(self, user_id: int) -> Optional[User]:
        """Obtiene un usuario por su ID usando el servicio externo"""
        return self.external_service.get_user(user_id)

class BookRepositoryAdapter(BookRepositoryPort):
    """Adaptador del repositorio de libros usando servicios externos"""
    
    def __init__(self):
        self.external_service = ExternalBookServiceAdapter()
    
    def get_by_id(self, book_id: int) -> Optional[Book]:
        """Obtiene un libro por su ID usando el servicio externo"""
        return self.external_service.get_book(book_id)
    
    def mark_as_loaned(self, book_id: int) -> bool:
        """Marca un libro como prestado usando el servicio externo"""
        return self.external_service.mark_book_as_loaned(book_id)
    
    def mark_as_available(self, book_id: int) -> bool:
        """Marca un libro como disponible usando el servicio externo"""
        return self.external_service.mark_book_as_available(book_id)

class LoanRepositoryAdapter(LoanRepositoryPort):
    """Adaptador del repositorio de préstamos usando Django ORM"""
    
    def save(self, loan: Loan) -> Loan:
        """Guarda un préstamo en la base de datos"""
        from loans.models import LoanModel
        
        if loan.id:
            # Actualizar préstamo existente
            loan_model = LoanModel.objects.get(id=loan.id)
            loan_model.user_id = loan.user_id
            loan_model.book_id = loan.book_id
            loan_model.start_date = loan.start_date
            loan_model.due_date = loan.due_date
            loan_model.return_date = loan.return_date
            loan_model.status = loan.status.value
            loan_model.save()
        else:
            # Crear nuevo préstamo
            loan_model = LoanModel.objects.create(
                user_id=loan.user_id,
                book_id=loan.book_id,
                start_date=loan.start_date,
                due_date=loan.due_date,
                return_date=loan.return_date,
                status=loan.status.value
            )
            loan.id = loan_model.id
        
        return loan
    
    def get_by_id(self, loan_id: int) -> Optional[Loan]:
        """Obtiene un préstamo por su ID"""
        from loans.models import LoanModel
        
        try:
            loan_model = LoanModel.objects.get(id=loan_id)
            return self._model_to_entity(loan_model)
        except LoanModel.DoesNotExist:
            return None
    
    def get_active_loans_by_user(self, user_id: int) -> List[Loan]:
        """Obtiene todos los préstamos activos de un usuario"""
        from loans.models import LoanModel
        
        loan_models = LoanModel.objects.filter(
            user_id=user_id,
            status='active'
        )
        return [self._model_to_entity(loan_model) for loan_model in loan_models]
    
    def get_all_active_loans(self) -> List[Loan]:
        """Obtiene todos los préstamos activos"""
        from loans.models import LoanModel
        
        loan_models = LoanModel.objects.filter(status='active')
        return [self._model_to_entity(loan_model) for loan_model in loan_models]
    
    def _model_to_entity(self, loan_model) -> Loan:
        """Convierte un modelo Django a una entidad del dominio"""
        return Loan(
            id=loan_model.id,
            user_id=loan_model.user_id,
            book_id=loan_model.book_id,
            start_date=loan_model.start_date,
            due_date=loan_model.due_date,
            return_date=loan_model.return_date,
            status=LoanStatus(loan_model.status)
        )