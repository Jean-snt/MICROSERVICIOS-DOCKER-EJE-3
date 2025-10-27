"""
Infrastructure Layer - Servicios externos
Implementaciones concretas de servicios externos
"""
from ..domain.entities import User
from ..domain.ports import UserService


class EmailService(UserService):
    """
    Adaptador - Implementación del servicio de email
    """
    
    def send_welcome_email(self, user: User) -> bool:
        """
        Enviar email de bienvenida al usuario
        En una implementación real, aquí se integraría con un servicio de email
        """
        try:
            # Simular envío de email
            print(f"📧 Enviando email de bienvenida a {user.email}")
            print(f"   Hola {user.name}, ¡bienvenido a nuestro sistema!")
            
            # En una implementación real:
            # - Usar SendGrid, AWS SES, etc.
            # - Enviar email asíncrono con Celery
            # - Manejar errores de entrega
            
            return True
            
        except Exception as e:
            print(f"❌ Error enviando email a {user.email}: {e}")
            return False


class MockEmailService(UserService):
    """
    Adaptador - Implementación mock del servicio de email para testing
    """
    
    def __init__(self):
        self.sent_emails = []

    def send_welcome_email(self, user: User) -> bool:
        """Mock del envío de email"""
        self.sent_emails.append({
            'user_id': user.id,
            'email': user.email,
            'name': user.name
        })
        return True


