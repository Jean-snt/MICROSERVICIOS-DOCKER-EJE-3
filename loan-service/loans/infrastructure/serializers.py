"""
CAPA DE INFRAESTRUCTURA - SERIALIZERS
Serializadores para la API REST (adaptadores de entrada/salida HTTP)
"""
from rest_framework import serializers
from ..domain.entities import LoanEntity


class LoanSerializer(serializers.Serializer):
    """
    Serializador para la entidad Loan
    Adaptador que traduce entre entidades de dominio y JSON
    """
    id = serializers.IntegerField(read_only=True)
    user_id = serializers.IntegerField()
    book_id = serializers.IntegerField()
    start_date = serializers.DateField(read_only=True)
    due_date = serializers.DateField(read_only=True)
    return_date = serializers.DateField(read_only=True, allow_null=True)
    status = serializers.CharField(read_only=True)
    
    def to_entity(self) -> LoanEntity:
        """Convierte datos validados a entidad de dominio"""
        return LoanEntity(
            user_id=self.validated_data['user_id'],
            book_id=self.validated_data['book_id'],
            start_date=self.validated_data.get('start_date'),
            due_date=self.validated_data.get('due_date'),
            status=self.validated_data.get('status', 'active')
        )
    
    @staticmethod
    def from_entity(entity: LoanEntity) -> dict:
        """Convierte entidad de dominio a diccionario serializable"""
        return {
            'id': entity.id,
            'user_id': entity.user_id,
            'book_id': entity.book_id,
            'start_date': entity.start_date.isoformat() if entity.start_date else None,
            'due_date': entity.due_date.isoformat() if entity.due_date else None,
            'return_date': entity.return_date.isoformat() if entity.return_date else None,
            'status': entity.status
        }


class CreateLoanRequestSerializer(serializers.Serializer):
    """Serializador para la request de creación de préstamo"""
    user_id = serializers.IntegerField(min_value=1)
    book_id = serializers.IntegerField(min_value=1)