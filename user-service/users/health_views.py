"""
Vistas de health check para el microservicio
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import connection


class HealthCheckView(APIView):
    """
    Endpoint de health check para verificar el estado del servicio
    """
    
    def get(self, request):
        """Verifica el estado del servicio"""
        try:
            # Verificar conexión a la base de datos
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            
            return Response({
                'status': 'healthy',
                'service': 'user-service',
                'database': 'connected'
            })
        except Exception as e:
            return Response({
                'status': 'unhealthy',
                'service': 'user-service',
                'error': str(e)
            }, status=503)





