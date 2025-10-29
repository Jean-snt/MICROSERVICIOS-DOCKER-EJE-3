import datetime

class Loan:
    def __init__(self, user_id: int, book_id: int, loan_date: datetime.date, due_date: datetime.date, id: int = None):
        self.id = id
        self.user_id = user_id
        self.book_id = book_id
        self.loan_date = loan_date
        self.due_date = due_date

    def is_overdue(self):
        return datetime.date.today() > self.due_date