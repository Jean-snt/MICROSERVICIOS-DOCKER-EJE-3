from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    """
    Serializador para convertir objetos User a/desde formato JSON.
    """
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'is_active', 'created_at']