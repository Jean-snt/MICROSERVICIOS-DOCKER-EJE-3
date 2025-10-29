import datetime
from loans.domain.loan import Loan
from .ports.loan_repository import LoanRepository
from .ports.user_service import UserService
from .ports.book_service import BookService

class LoanApplicationService:
    def __init__(self, loan_repository: LoanRepository, user_service: UserService, book_service: BookService):
        self.loan_repository = loan_repository
        self.user_service = user_service
        self.book_service = book_service

    def create_loan(self, user_id: int, book_id: int) -> Loan:
        # Validate user
        user = self.user_service.get_user(user_id)
        if not user or not user['is_active'] or user['is_suspended']:
            raise Exception("Invalid or inactive user")

        # Validate book
        book = self.book_service.get_book(book_id)
        if not book or book['status'] != 'available' or book['is_deleted']:
            raise Exception("Book not available")

        # Check user's active loans
        active_loans = self.loan_repository.get_loans_by_user(user_id)
        if len(active_loans) >= 3:
            raise Exception("User has reached the maximum number of active loans")

        # Create loan
        loan_date = datetime.date.today()
        due_date = loan_date + datetime.timedelta(days=15)
        loan = Loan(user_id=user_id, book_id=book_id, loan_date=loan_date, due_date=due_date)
        
        # Save loan and update book status
        created_loan = self.loan_repository.create_loan(loan)
        self.book_service.update_book_status(book_id, 'prestado')
        
        return created_loan

    def get_all_loans(self) -> list[Loan]:
        return self.loan_repository.get_all()