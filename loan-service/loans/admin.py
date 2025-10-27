from django.contrib import admin
from .models import Loan


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'book_id', 'start_date', 'due_date', 'status']
    list_filter = ['status', 'start_date']
    search_fields = ['user_id', 'book_id']
    readonly_fields = ['created_at']



