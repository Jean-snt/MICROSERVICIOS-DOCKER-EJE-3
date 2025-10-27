from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def home_view(request):
    return JsonResponse({
        'service': 'Microservicio de Usuarios',
        'version': '1.0.0',
        'description': 'Gestión de usuarios del sistema de biblioteca digital',
        'endpoints': {
            'users': '/api/users/',
            'admin': '/admin/'
        },
        'status': 'running'
    })

urlpatterns = [
    path('', home_view, name='home'),
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
]
