"""
CAPA DE INFRAESTRUCTURA - ADAPTADORES DE PERSISTENCIA
Implementan los puertos del dominio usando Django ORM
"""
from typing import List, Optional
from ..domain.entities import LoanEntity
from ..domain.ports import LoanRepositoryPort
from ..models import Loan


class DjangoLoanRepository(LoanRepositoryPort):
    """
    Adaptador de salida: Implementa el puerto del repositorio usando Django ORM
    Traduce entre entidades de dominio y modelos de Django
    """
    
    def _to_entity(self, model: Loan) -> LoanEntity:
        """Convierte un modelo Django a una entidad de dominio"""
        return LoanEntity(
            id=model.id,
            user_id=model.user_id,
            book_id=model.book_id,
            start_date=model.start_date,
            due_date=model.due_date,
            return_date=model.return_date,
            status=model.status
        )
    
    def _to_model(self, entity: LoanEntity, model: Optional[Loan] = None) -> Loan:
        """Convierte una entidad de dominio a un modelo Django"""
        if model is None:
            model = Loan()
        
        model.user_id = entity.user_id
        model.book_id = entity.book_id
        model.start_date = entity.start_date
        model.due_date = entity.due_date
        model.return_date = entity.return_date
        model.status = entity.status
        
        return model
    
    def save(self, loan: LoanEntity) -> LoanEntity:
        """Guarda un nuevo préstamo"""
        model = self._to_model(loan)
        model.save()
        return self._to_entity(model)
    
    def find_by_id(self, loan_id: int) -> Optional[LoanEntity]:
        """Busca un préstamo por ID"""
        try:
            model = Loan.objects.get(id=loan_id)
            return self._to_entity(model)
        except Loan.DoesNotExist:
            return None
    
    def find_active_by_user(self, user_id: int) -> List[LoanEntity]:
        """Encuentra préstamos activos de un usuario"""
        models = Loan.objects.filter(user_id=user_id, status='active')
        return [self._to_entity(model) for model in models]
    
    def find_by_book(self, book_id: int) -> List[LoanEntity]:
        """Encuentra todos los préstamos de un libro"""
        models = Loan.objects.filter(book_id=book_id)
        return [self._to_entity(model) for model in models]
    
    def find_all(self) -> List[LoanEntity]:
        """Obtiene todos los préstamos"""
        models = Loan.objects.all()
        return [self._to_entity(model) for model in models]
    
    def update(self, loan: LoanEntity) -> LoanEntity:
        """Actualiza un préstamo existente"""
        try:
            model = Loan.objects.get(id=loan.id)
            model = self._to_model(loan, model)
            model.save()
            return self._to_entity(model)
        except Loan.DoesNotExist:
            raise ValueError(f"Préstamo con ID {loan.id} no existe")





