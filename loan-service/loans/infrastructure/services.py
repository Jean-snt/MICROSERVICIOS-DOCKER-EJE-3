"""
CAPA DE INFRAESTRUCTURA - ADAPTADORES DE SERVICIOS EXTERNOS
Implementan los puertos para comunicación con otros microservicios
"""
import requests
from typing import Optional
from django.conf import settings
from ..domain.entities import UserEntity, BookEntity
from ..domain.ports import UserServicePort, BookServicePort


class HttpUserService(UserServicePort):
    """
    Adaptador de salida: Implementa comunicación HTTP con el servicio de usuarios
    """
    
    def __init__(self):
        self.base_url = settings.USER_SERVICE_URL
    
    def get_user(self, user_id: int) -> Optional[UserEntity]:
        """Obtiene información de un usuario del servicio externo"""
        try:
            response = requests.get(
                f"{self.base_url}/api/users/{user_id}/",
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                return UserEntity(
                    id=data['id'],
                    email=data['email'],
                    is_active=data.get('is_active', True),
                    is_suspended=data.get('is_suspended', False)
                )
            
            return None
            
        except requests.RequestException as e:
            print(f"Error al comunicarse con user-service: {e}")
            return None
    
    def verify_user_exists(self, user_id: int) -> bool:
        """Verifica si un usuario existe"""
        user = self.get_user(user_id)
        return user is not None


class HttpBookService(BookServicePort):
    """
    Adaptador de salida: Implementa comunicación HTTP con el servicio de libros
    """
    
    def __init__(self):
        self.base_url = settings.BOOK_SERVICE_URL
    
    def get_book(self, book_id: int) -> Optional[BookEntity]:
        """Obtiene información de un libro del servicio externo"""
        try:
            response = requests.get(
                f"{self.base_url}/api/books/{book_id}/",
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                return BookEntity(
                    id=data['id'],
                    title=data['title'],
                    is_available=data.get('is_available', False),
                    is_deleted=data.get('is_deleted', False)
                )
            
            return None
            
        except requests.RequestException as e:
            print(f"Error al comunicarse con book-service: {e}")
            return None
    
    def verify_book_availability(self, book_id: int) -> bool:
        """Verifica si un libro está disponible"""
        book = self.get_book(book_id)
        return book is not None and book.is_available
    
    def mark_book_as_loaned(self, book_id: int) -> bool:
        """Marca un libro como prestado"""
        try:
            response = requests.patch(
                f"{self.base_url}/api/books/{book_id}/mark_loaned/",
                timeout=5
            )
            return response.status_code == 200
            
        except requests.RequestException as e:
            print(f"Error al marcar libro como prestado: {e}")
            return False
    
    def mark_book_as_available(self, book_id: int) -> bool:
        """Marca un libro como disponible"""
        try:
            response = requests.patch(
                f"{self.base_url}/api/books/{book_id}/mark_available/",
                timeout=5
            )
            return response.status_code == 200
            
        except requests.RequestException as e:
            print(f"Error al marcar libro como disponible: {e}")
            return False





