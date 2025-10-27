from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def home_view(request):
    return JsonResponse({
        'service': 'Microservicio de Préstamos',
        'version': '1.0.0',
        'description': 'Gestión de préstamos con Arquitectura Hexagonal',
        'architecture': 'Hexagonal (Ports and Adapters)',
        'endpoints': {
            'loans': '/api/loans/',
            'admin': '/admin/'
        },
        'business_rules': [
            'Máximo 3 préstamos activos por usuario',
            'Préstamos por 15 días',
            'Usuarios suspendidos no pueden pedir préstamos',
            'Libros eliminados no están disponibles'
        ],
        'status': 'running'
    })

urlpatterns = [
    path('', home_view, name='home'),
    path('admin/', admin.site.urls),
    path('api/loans/', include('loans.urls')),
]
