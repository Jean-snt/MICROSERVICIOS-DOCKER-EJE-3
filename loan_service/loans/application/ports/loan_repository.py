from abc import ABC, abstractmethod
from typing import List
from loans.domain.loan import Loan

class LoanRepository(ABC):
    @abstractmethod
    def create_loan(self, loan: Loan) -> Loan:
        pass

    @abstractmethod
    def get_loans_by_user(self, user_id: int) -> List[Loan]:
        pass

    @abstractmethod
    def get_all(self) -> List[Loan]:
        pass