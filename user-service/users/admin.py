from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'full_name', 'membership_number', 'is_active', 'is_suspended']
    list_filter = ['is_active', 'is_suspended', 'membership_date']
    search_fields = ['email', 'first_name', 'last_name', 'membership_number']
    readonly_fields = ['created_at', 'updated_at', 'membership_date']
