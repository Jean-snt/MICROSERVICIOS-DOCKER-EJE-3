from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Book
from .serializers import BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar libros"""
    
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    @action(detail=True, methods=['get'])
    def check_availability(self, request, pk=None):
        """Endpoint para verificar la disponibilidad de un libro"""
        book = get_object_or_404(Book, pk=pk)
        
        return Response({
            'book_id': book.id,
            'is_available': book.is_available,
            'is_loaned': book.is_loaned,
            'is_deleted': book.is_deleted,
            'status': book.status
        })
    
    @action(detail=True, methods=['post'])
    def mark_as_loaned(self, request, pk=None):
        """Endpoint para marcar un libro como prestado"""
        book = get_object_or_404(Book, pk=pk)
        
        if book.is_deleted:
            return Response(
                {'error': 'No se puede prestar un libro eliminado'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        book.status = 'loaned'
        book.save()
        
        serializer = self.get_serializer(book)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def mark_as_available(self, request, pk=None):
        """Endpoint para marcar un libro como disponible"""
        book = get_object_or_404(Book, pk=pk)
        book.status = 'available'
        book.save()
        
        serializer = self.get_serializer(book)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def delete_book(self, request, pk=None):
        """Endpoint para eliminar un libro (soft delete)"""
        book = get_object_or_404(Book, pk=pk)
        book.status = 'deleted'
        book.save()
        
        serializer = self.get_serializer(book)
        return Response(serializer.data)
