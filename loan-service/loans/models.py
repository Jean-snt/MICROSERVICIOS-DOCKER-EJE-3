"""
Modelos de base de datos - Capa de Infraestructura
Estos modelos son adaptadores de persistencia de Django ORM
"""
from django.db import models


class Loan(models.Model):
    """
    Modelo de persistencia para Préstamos
    Este es un adaptador que mapea la entidad de dominio a la BD
    """
    STATUS_CHOICES = [
        ('active', 'Activo'),
        ('returned', 'Devuelto'),
        ('overdue', 'Vencido'),
    ]
    
    user_id = models.IntegerField(help_text="ID del usuario en el microservicio de usuarios")
    book_id = models.IntegerField(help_text="ID del libro en el microservicio de libros")
    start_date = models.DateField()
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'loans'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user_id', 'status']),
            models.Index(fields=['book_id']),
        ]
    
    def __str__(self):
        return f"Préstamo #{self.id} - Usuario {self.user_id} - Libro {self.book_id}"



