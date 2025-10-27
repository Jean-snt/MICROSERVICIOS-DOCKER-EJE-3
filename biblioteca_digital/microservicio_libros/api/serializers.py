from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    """
    Serializador para convertir objetos Book a/desde formato JSON.
    """
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'status', 'is_deleted']