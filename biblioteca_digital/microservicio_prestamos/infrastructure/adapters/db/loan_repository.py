from typing import List, Optional
from domain.models.loan import Loan
from domain.ports import LoanRepositoryPort
from .models import LoanModel

class DjangoLoanRepository(LoanRepositoryPort):
    """
    Implementación del puerto de repositorio de préstamos
    utilizando el ORM de Django.
    """
    def save(self, loan: Loan) -> Loan:
        loan_model = LoanModel.objects.create(
            user_id=loan.user_id,
            book_id=loan.book_id,
            loan_date=loan.loan_date,
            due_date=loan.due_date,
            status=loan.status
        )
        loan.id = loan_model.id
        return loan

    def find_by_id(self, loan_id: int) -> Optional[Loan]:
        try:
            loan_model = LoanModel.objects.get(pk=loan_id)
            return Loan(
                id=loan_model.id,
                user_id=loan_model.user_id,
                book_id=loan_model.book_id,
                loan_date=loan_model.loan_date,
                due_date=loan_model.due_date,
                status=loan_model.status
            )
        except LoanModel.DoesNotExist:
            return None

    def find_active_by_user_id(self, user_id: int) -> List[Loan]:
        active_loans_models = LoanModel.objects.filter(user_id=user_id, status="activo")
        return [
            Loan(
                id=model.id,
                user_id=model.user_id,
                book_id=model.book_id,
                loan_date=model.loan_date,
                due_date=model.due_date,
                status=model.status
            )
            for model in active_loans_models
        ]