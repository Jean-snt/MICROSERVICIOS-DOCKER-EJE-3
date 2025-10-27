"""
URL configuration for loan_service project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('loans.urls')),
    path('health/', include('loans.health_urls')),
]
