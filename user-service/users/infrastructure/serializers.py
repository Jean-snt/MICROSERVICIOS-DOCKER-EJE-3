"""
Infrastructure Layer - Serializers
Para la serialización/deserialización de datos
"""
from rest_framework import serializers
from ..domain.entities import User


class UserSerializer(serializers.Serializer):
    """
    Serializer para la entidad User
    """
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def validate_name(self, value):
        """Validar nombre"""
        if not value or not value.strip():
            raise serializers.ValidationError("El nombre es requerido")
        return value.strip()

    def validate_email(self, value):
        """Validar email"""
        if not value or not value.strip():
            raise serializers.ValidationError("El email es requerido")
        return value.strip().lower()

    def create(self, validated_data):
        """Crear usuario desde datos validados"""
        return User.create(
            name=validated_data['name'],
            email=validated_data['email']
        )

    def update(self, instance, validated_data):
        """Actualizar usuario desde datos validados"""
        if 'name' in validated_data:
            instance.update_name(validated_data['name'])
        if 'email' in validated_data:
            instance.update_email(validated_data['email'])
        return instance


class CreateUserSerializer(serializers.Serializer):
    """
    Serializer específico para crear usuarios
    """
    name = serializers.CharField(max_length=255)
    email = serializers.EmailField()

    def validate_name(self, value):
        """Validar nombre"""
        if not value or not value.strip():
            raise serializers.ValidationError("El nombre es requerido")
        return value.strip()

    def validate_email(self, value):
        """Validar email"""
        if not value or not value.strip():
            raise serializers.ValidationError("El email es requerido")
        return value.strip().lower()


class UpdateUserSerializer(serializers.Serializer):
    """
    Serializer específico para actualizar usuarios
    """
    name = serializers.CharField(max_length=255, required=False)
    email = serializers.EmailField(required=False)

    def validate_name(self, value):
        """Validar nombre"""
        if value is not None and (not value or not value.strip()):
            raise serializers.ValidationError("El nombre no puede estar vacío")
        return value.strip() if value else value

    def validate_email(self, value):
        """Validar email"""
        if value is not None and (not value or not value.strip()):
            raise serializers.ValidationError("El email no puede estar vacío")
        return value.strip().lower() if value else value


