from django.contrib import admin
from .models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'isbn', 'is_available', 'is_deleted']
    list_filter = ['is_available', 'is_deleted', 'genre']
    search_fields = ['title', 'author', 'isbn']
    readonly_fields = ['created_at', 'updated_at']





