from rest_framework import generics
from .models import Book
from .serializers import BookSerializer

class BookListCreateView(generics.ListCreateAPIView):
    """
    Vista para listar todos los libros y crear uno nuevo.
    """
    queryset = Book.objects.filter(is_deleted=False)
    serializer_class = BookSerializer

class BookDetailView(generics.RetrieveUpdateAPIView):
    """
    Vista para recuperar y actualizar un libro específico.
    """
    queryset = Book.objects.filter(is_deleted=False)
    serializer_class = BookSerializer
