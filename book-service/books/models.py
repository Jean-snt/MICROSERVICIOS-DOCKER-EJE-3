"""
Modelos para el microservicio de libros
"""
from django.db import models


class Book(models.Model):
    """
    Modelo de Libro
    """
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True)
    publisher = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    genre = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_available = models.BooleanField(default=True, help_text="Disponible para préstamo")
    is_deleted = models.BooleanField(default=False, help_text="Marcado como eliminado")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'books'
        ordering = ['title']
        indexes = [
            models.Index(fields=['isbn']),
            models.Index(fields=['is_available', 'is_deleted']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.author}"





