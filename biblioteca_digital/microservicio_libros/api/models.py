from django.db import models

# Create your models here.
from django.db import models

class Book(models.Model):
    """
    Representa un libro digital en el sistema.
    """
    STATUS_CHOICES = [
        ('disponible', 'Disponible'),
        ('prestado', 'Prestado'),
    ]

    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='disponible')
    is_deleted = models.BooleanField(default=False) # Para borrado lógico

    def __str__(self):
        return self.title
