from django.db import models

class Book(models.Model):
    """Modelo de Libro para el microservicio de libros"""
    
    STATUS_CHOICES = [
        ('available', 'Disponible'),
        ('loaned', 'Prestado'),
        ('deleted', 'Eliminado'),
    ]
    
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13, unique=True)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'books'
        verbose_name = 'Libro'
        verbose_name_plural = 'Libros'
    
    def __str__(self):
        return f"{self.title} - {self.author}"
    
    @property
    def is_available(self):
        """Verifica si el libro está disponible para préstamo"""
        return self.status == 'available'
    
    @property
    def is_loaned(self):
        """Verifica si el libro está prestado"""
        return self.status == 'loaned'
    
    @property
    def is_deleted(self):
        """Verifica si el libro está eliminado"""
        return self.status == 'deleted'
