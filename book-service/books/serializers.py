"""
Serializadores para el microservicio de libros
"""
from rest_framework import serializers
from .models import Book


class BookSerializer(serializers.ModelSerializer):
    """
    Serializador completo para el modelo Book
    """
    class Meta:
        model = Book
        fields = [
            'id', 'title', 'author', 'isbn', 'publisher',
            'publication_year', 'genre', 'description',
            'is_available', 'is_deleted', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class BookListSerializer(serializers.ModelSerializer):
    """
    Serializador simplificado para listados
    """
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'isbn', 'is_available', 'is_deleted']





