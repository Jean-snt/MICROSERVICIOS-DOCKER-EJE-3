from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from datetime import datetime

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

def healthz_view(request):
    return JsonResponse({
        'status': 'healthy',
        'service': 'loans-service',
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })

urlpatterns = [
    path('', home_view, name='home'),
    path('healthz/', healthz_view, name='healthz'),
    path('admin/', admin.site.urls),
    path('api/loans/', include('loans.urls')),
]
