# Contenido completo para loans/infrastructure/loans_repository.py
from typing import Optional, List
from django.db.models import Count
import uuid

# Importaciones de capas internas
from ..port.ports import LoansRepositoryPort  
from ..domain.models import Loan              
from .models import LoanModel                 

class DjangoLoanRepository(LoansRepositoryPort):
    """
    Adaptador de Repositorio para Préstamos que usa el Django ORM.
    Implementa el contrato (Puerto) LoansRepositoryPort.
    """

    def _to_domain(self, model: LoanModel) -> Loan:
        """Mapea un modelo ORM a una entidad de Dominio."""
        return Loan(
            id=str(model.id),
            user_id=model.user_id,
            book_id=model.book_id,
            start_date=model.start_date,
            due_date=model.due_date,
            return_date=model.return_date,
        )

    def _to_model(self, loan: Loan) -> LoanModel:
        """Mapea una entidad de Dominio a un modelo ORM."""
        if not loan.id:
            loan.id = str(uuid.uuid4()) 

        return LoanModel(
            id=loan.id,
            user_id=loan.user_id,
            book_id=loan.book_id,
            start_date=loan.start_date,
            due_date=loan.due_date,
            return_date=loan.return_date,
        )

    # Implementación de los métodos del puerto
    # Nota: El nombre 'get_by_id' aquí debe coincidir con el puerto si se usa un repositorio genérico.
    # Si tu puerto define get_loan_by_id, debes usar ese nombre aquí. Usaré get_by_id basado en tu código anterior.
    
    def get_loan_by_id(self, loan_id: str) -> Optional[Loan]:
        """Recupera un Préstamo por su ID."""
        try:
            model = LoanModel.objects.get(id=loan_id)
            return self._to_domain(model)
        except LoanModel.DoesNotExist:
            return None

    def create_loan(self, loan: Loan) -> Loan:
        """Guarda un nuevo Préstamo."""
        if not loan.id:
            loan.id = str(uuid.uuid4())
            
        model = self._to_model(loan)
        model.save()
        return self._to_domain(model)

    def update_loan_status(self, loan_id: str, new_status: str) -> Loan:
        """Actualiza el estado de un préstamo (asumiendo que se hace a través de 'save' en la entidad)."""
        # Ya que tu modelo no tiene un campo 'status' y el estado se infiere de 'return_date',
        # este método puede ser más complejo o simplemente se delega a 'save' después de modificar la entidad.
        # Por simplicidad, aquí se usa 'save' para actualizar si la entidad se modifica antes de llamar.
        raise NotImplementedError("Actualizar el estado del préstamo requiere modificar la entidad y usar 'save'.")

    def get_active_loans_by_user(self, user_id: str) -> List[Loan]:
        """Recupera todos los préstamos activos para un usuario específico (return_date es nulo)."""
        models = LoanModel.objects.filter(user_id=user_id, return_date__isnull=True)
        return [self._to_domain(model) for model in models]

    def count_active_loans(self, user_id: str) -> int:
        """Cuenta el número de préstamos activos para un usuario."""
        return LoanModel.objects.filter(user_id=user_id, return_date__isnull=True).count()