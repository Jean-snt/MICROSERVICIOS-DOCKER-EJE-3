from django.db import models

class LoanModel(models.Model):
    """
    Representa la tabla 'loan' en la base de datos usando el ORM de Django.
    """
    user_id = models.IntegerField()
    book_id = models.IntegerField()
    loan_date = models.DateField()
    due_date = models.DateField()
    status = models.CharField(max_length=20)

    class Meta:
        db_table = 'loans' # Nombre de la tabla en la base de datos