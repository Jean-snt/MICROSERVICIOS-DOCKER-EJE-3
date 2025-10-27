from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Book"""
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'isbn', 'description', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_isbn(self, value):
        """Valida que el ISBN sea único"""
        if Book.objects.filter(isbn=value).exists():
            raise serializers.ValidationError("Este ISBN ya está registrado.")
        return value
