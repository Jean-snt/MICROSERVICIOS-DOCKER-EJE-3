from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('prestado', 'Prestado'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='available')
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title
