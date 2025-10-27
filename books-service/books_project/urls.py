from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

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

urlpatterns = [
    path('', home_view, name='home'),
    path('admin/', admin.site.urls),
    path('api/books/', include('books.urls')),
]
