from django.db import models

class User(models.Model):
    """
    Representa a un usuario en el sistema de la biblioteca digital.
    """
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
