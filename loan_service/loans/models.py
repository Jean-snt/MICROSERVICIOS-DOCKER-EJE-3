from django.db import models

class Loan(models.Model):
    user_id = models.IntegerField()
    book_id = models.IntegerField()
    loan_date = models.DateField()
    due_date = models.DateField()

    def __str__(self):
        return f"Loan {self.id} - User {self.user_id}, Book {self.book_id}"
