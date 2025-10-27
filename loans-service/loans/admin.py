from django.contrib import admin
from .models import LoanModel

@admin.register(LoanModel)
class LoanAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'book_id', 'start_date', 'due_date', 'status', 'created_at']
    list_filter = ['status', 'start_date', 'created_at']
    search_fields = ['user_id', 'book_id']
    readonly_fields = ['created_at', 'updated_at']
