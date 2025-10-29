from typing import List
from loans.application.ports.loan_repository import LoanRepository
from loans.domain.loan import Loan as DomainLoan
from loans.models import Loan as DjangoLoan

class DjangoLoanRepository(LoanRepository):
    def create_loan(self, loan: DomainLoan) -> DomainLoan:
        django_loan = DjangoLoan.objects.create(
            user_id=loan.user_id,
            book_id=loan.book_id,
            loan_date=loan.loan_date,
            due_date=loan.due_date
        )
        return self._to_domain(django_loan)

    def get_loans_by_user(self, user_id: int) -> List[DomainLoan]:
        django_loans = DjangoLoan.objects.filter(user_id=user_id)
        return [self._to_domain(loan) for loan in django_loans]

    def get_all(self) -> List[DomainLoan]:
        django_loans = DjangoLoan.objects.all()
        return [self._to_domain(loan) for loan in django_loans]

    def _to_domain(self, django_loan: DjangoLoan) -> DomainLoan:
        return DomainLoan(
            id=django_loan.id,
            user_id=django_loan.user_id,
            book_id=django_loan.book_id,
            loan_date=django_loan.loan_date,
            due_date=django_loan.due_date
        )