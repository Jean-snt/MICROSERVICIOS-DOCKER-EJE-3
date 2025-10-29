from loans.application.loan_service import LoanApplicationService
from loans.infrastructure.repositories.django_loan_repository import DjangoLoanRepository
from loans.infrastructure.services.user_service_adapter import UserServiceAdapter
from loans.infrastructure.services.book_service_adapter import BookServiceAdapter

def get_loan_service():
    loan_repository = DjangoLoanRepository()
    user_service = UserServiceAdapter()
    book_service = BookServiceAdapter()
    return LoanApplicationService(loan_repository, user_service, book_service)