"""
Serializadores para el microservicio de usuarios
"""
from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Serializador completo para el modelo User
    """
    full_name = serializers.ReadOnlyField()
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name', 'full_name',
            'phone', 'address', 'membership_number', 'membership_date',
            'is_active', 'is_suspended', 'suspension_reason',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'membership_date', 'created_at', 'updated_at']


class UserListSerializer(serializers.ModelSerializer):
    """
    Serializador simplificado para listados
    """
    full_name = serializers.ReadOnlyField()
    
    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'membership_number', 'is_active', 'is_suspended']


class CreateUserSerializer(serializers.ModelSerializer):
    """
    Serializador para crear usuarios
    """
    class Meta:
        model = User
        fields = [
            'email', 'first_name', 'last_name', 'phone', 
            'address', 'membership_number'
        ]





