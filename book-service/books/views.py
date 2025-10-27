"""
Vistas para el microservicio de libros
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Book
from .serializers import BookSerializer, BookListSerializer


class BookListCreateView(APIView):
    """
    GET: Lista todos los libros
    POST: Crea un nuevo libro
    """
    
    def get(self, request):
        """Lista libros disponibles (no eliminados)"""
        include_deleted = request.query_params.get('include_deleted', 'false').lower() == 'true'
        
        if include_deleted:
            books = Book.objects.all()
        else:
            books = Book.objects.filter(is_deleted=False)
        
        serializer = BookListSerializer(books, many=True)
        
        return Response({
            'success': True,
            'books': serializer.data,
            'count': len(serializer.data)
        })
    
    def post(self, request):
        """Crea un nuevo libro"""
        serializer = BookSerializer(data=request.data)
        
        if serializer.is_valid():
            book = serializer.save()
            return Response({
                'success': True,
                'book': serializer.data,
                'message': 'Libro creado exitosamente'
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'success': False,
            'error': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class BookDetailView(APIView):
    """
    GET: Obtiene detalles de un libro
    PUT: Actualiza un libro
    DELETE: Marca un libro como eliminado (soft delete)
    """
    
    def get(self, request, book_id):
        """Obtiene un libro por ID"""
        book = get_object_or_404(Book, id=book_id)
        serializer = BookSerializer(book)
        
        return Response({
            'success': True,
            'book': serializer.data
        })
    
    def put(self, request, book_id):
        """Actualiza un libro"""
        book = get_object_or_404(Book, id=book_id)
        serializer = BookSerializer(book, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'book': serializer.data,
                'message': 'Libro actualizado exitosamente'
            })
        
        return Response({
            'success': False,
            'error': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, book_id):
        """Marca un libro como eliminado (soft delete)"""
        book = get_object_or_404(Book, id=book_id)
        book.is_deleted = True
        book.is_available = False
        book.save()
        
        return Response({
            'success': True,
            'message': 'Libro marcado como eliminado'
        })


class MarkBookLoanedView(APIView):
    """
    PATCH: Marca un libro como prestado
    """
    
    def patch(self, request, book_id):
        """Marca un libro como prestado"""
        book = get_object_or_404(Book, id=book_id)
        
        if book.is_deleted:
            return Response({
                'success': False,
                'error': 'No se puede prestar un libro eliminado'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if not book.is_available:
            return Response({
                'success': False,
                'error': 'El libro ya está prestado'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        book.is_available = False
        book.save()
        
        return Response({
            'success': True,
            'message': 'Libro marcado como prestado'
        })


class MarkBookAvailableView(APIView):
    """
    PATCH: Marca un libro como disponible
    """
    
    def patch(self, request, book_id):
        """Marca un libro como disponible"""
        book = get_object_or_404(Book, id=book_id)
        
        if not book.is_deleted:
            book.is_available = True
            book.save()
        
        return Response({
            'success': True,
            'message': 'Libro marcado como disponible'
        })


class AvailableBooksView(APIView):
    """
    GET: Lista libros disponibles para préstamo
    """
    
    def get(self, request):
        """Lista libros disponibles"""
        books = Book.objects.filter(is_available=True, is_deleted=False)
        serializer = BookListSerializer(books, many=True)
        
        return Response({
            'success': True,
            'books': serializer.data,
            'count': len(serializer.data)
        })





