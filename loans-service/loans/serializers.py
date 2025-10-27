from rest_framework import serializers
from .models import LoanModel

class LoanSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Loan"""
    
    class Meta:
        model = LoanModel
        fields = ['id', 'user_id', 'book_id', 'start_date', 'due_date', 'return_date', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class CreateLoanSerializer(serializers.Serializer):
    """Serializer para crear un préstamo"""
    user_id = serializers.IntegerField()
    book_id = serializers.IntegerField()
    
    def validate_user_id(self, value):
        """Valida que el user_id sea positivo"""
        if value <= 0:
            raise serializers.ValidationError("El ID de usuario debe ser positivo")
        return value
    
    def validate_book_id(self, value):
        """Valida que el book_id sea positivo"""
        if value <= 0:
            raise serializers.ValidationError("El ID de libro debe ser positivo")
        return value

class LoanEntitySerializer(serializers.Serializer):
    """Serializer para entidades del dominio Loan"""
    id = serializers.IntegerField(allow_null=True)
    user_id = serializers.IntegerField()
    book_id = serializers.IntegerField()
    start_date = serializers.DateTimeField()
    due_date = serializers.DateTimeField()
    return_date = serializers.DateTimeField(allow_null=True)
    status = serializers.CharField()
    
    def to_representation(self, instance):
        """Convierte la entidad del dominio a diccionario serializable"""
        return {
            'id': instance.id,
            'user_id': instance.user_id,
            'book_id': instance.book_id,
            'start_date': instance.start_date,
            'due_date': instance.due_date,
            'return_date': instance.return_date,
            'status': instance.status.value if hasattr(instance.status, 'value') else str(instance.status)
        }
