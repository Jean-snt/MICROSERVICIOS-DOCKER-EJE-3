"""
URLs del módulo de libros
"""
from django.urls import path
from .views import (
    BookListCreateView,
    BookDetailView,
    MarkBookLoanedView,
    MarkBookAvailableView,
    AvailableBooksView
)

urlpatterns = [
    path('books/', BookListCreateView.as_view(), name='book-list-create'),
    path('books/<int:book_id>/', BookDetailView.as_view(), name='book-detail'),
    path('books/<int:book_id>/mark_loaned/', MarkBookLoanedView.as_view(), name='book-mark-loaned'),
    path('books/<int:book_id>/mark_available/', MarkBookAvailableView.as_view(), name='book-mark-available'),
    path('books/available/', AvailableBooksView.as_view(), name='book-available'),
]





