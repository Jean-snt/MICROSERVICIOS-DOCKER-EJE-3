from django.db import models

class LoanModel(models.Model):
    """Modelo Django para préstamos"""
    
    STATUS_CHOICES = [
        ('active', 'Activo'),
        ('returned', 'Devuelto'),
        ('overdue', 'Vencido'),
    ]
    
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    book_id = models.IntegerField()
    start_date = models.DateTimeField()
    due_date = models.DateTimeField()
    return_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'loans'
        verbose_name = 'Préstamo'
        verbose_name_plural = 'Préstamos'
