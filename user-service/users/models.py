"""
Modelos para el microservicio de usuarios
"""
from django.db import models


class User(models.Model):
    """
    Modelo de Usuario para la biblioteca
    """
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    membership_number = models.CharField(max_length=50, unique=True)
    membership_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_suspended = models.BooleanField(default=False, help_text="Usuario suspendido no puede pedir préstamos")
    suspension_reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'users'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['membership_number']),
            models.Index(fields=['is_active', 'is_suspended']),
        ]
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
