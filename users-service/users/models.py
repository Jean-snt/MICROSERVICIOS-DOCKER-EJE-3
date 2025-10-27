from django.db import models

class User(models.Model):
    """Modelo de Usuario para el microservicio de usuarios"""
    
    STATUS_CHOICES = [
        ('active', 'Activo'),
        ('suspended', 'Suspendido'),
        ('inactive', 'Inactivo'),
    ]
    
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'users'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
    
    def __str__(self):
        return f"{self.name} ({self.email})"
    
    @property
    def is_active(self):
        """Verifica si el usuario está activo"""
        return self.status == 'active'
    
    @property
    def is_suspended(self):
        """Verifica si el usuario está suspendido"""
        return self.status == 'suspended'
