"""
Infrastructure Layer - Health Check Views
"""
from django.http import JsonResponse
from django.db import connection
from django.core.cache import cache
import time


def health_check(request):
    """
    Health check endpoint
    """
    try:
        # Verificar conexión a base de datos
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            db_status = "OK"
    except Exception as e:
        db_status = f"ERROR: {str(e)}"

    # Verificar cache (opcional)
    try:
        cache.set('health_check', 'test', 10)
        cache_status = "OK" if cache.get('health_check') == 'test' else "ERROR"
    except Exception as e:
        cache_status = f"ERROR: {str(e)}"

    health_data = {
        'status': 'OK' if db_status == 'OK' else 'ERROR',
        'service': 'User Service',
        'timestamp': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        'checks': {
            'database': db_status,
            'cache': cache_status
        }
    }

    status_code = 200 if health_data['status'] == 'OK' else 503
    return JsonResponse(health_data, status=status_code)


