from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from datetime import datetime

def home_view(request):
    return JsonResponse({
        'service': 'Microservicio de Libros',
        'version': '1.0.0',
        'description': 'Catálogo de libros digitales del sistema de biblioteca',
        'endpoints': {
            'books': '/api/books/',
            'admin': '/admin/'
        },
        'status': 'running'
    })

def healthz_view(request):
    return JsonResponse({
        'status': 'healthy',
        'service': 'books-service',
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })

urlpatterns = [
    path('', home_view, name='home'),
    path('healthz/', healthz_view, name='healthz'),
    path('admin/', admin.site.urls),
    path('api/books/', include('books.urls')),
]
