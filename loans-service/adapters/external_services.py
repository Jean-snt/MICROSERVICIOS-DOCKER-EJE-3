import requests
import os
from typing import Optional
from domain.entities import User, Book
from domain.ports import ExternalUserServicePort, ExternalBookServicePort

class ExternalUserServiceAdapter(ExternalUserServicePort):
    """Adaptador para comunicarse con el microservicio de usuarios"""
    
    def __init__(self):
        self.base_url = os.getenv('USERS_SERVICE_URL', 'http://users-service:8000')
    
    def get_user(self, user_id: int) -> Optional[User]:
        """Obtiene un usuario del microservicio de usuarios"""
        try:
            response = requests.get(f"{self.base_url}/api/users/{user_id}/")
            if response.status_code == 200:
                data = response.json()
                return User(
                    id=data['id'],
                    name=data['name'],
                    email=data['email'],
                    status=data['status']
                )
            return None
        except requests.RequestException:
            return None

class ExternalBookServiceAdapter(ExternalBookServicePort):
    """Adaptador para comunicarse con el microservicio de libros"""
    
    def __init__(self):
        self.base_url = os.getenv('BOOKS_SERVICE_URL', 'http://books-service:8000')
    
    def get_book(self, book_id: int) -> Optional[Book]:
        """Obtiene un libro del microservicio de libros"""
        try:
            response = requests.get(f"{self.base_url}/api/books/{book_id}/")
            if response.status_code == 200:
                data = response.json()
                return Book(
                    id=data['id'],
                    title=data['title'],
                    author=data['author'],
                    isbn=data['isbn'],
                    status=data['status']
                )
            return None
        except requests.RequestException:
            return None
    
    def mark_book_as_loaned(self, book_id: int) -> bool:
        """Marca un libro como prestado en el microservicio de libros"""
        try:
            response = requests.post(f"{self.base_url}/api/books/{book_id}/mark_as_loaned/")
            return response.status_code == 200
        except requests.RequestException:
            return False
    
    def mark_book_as_available(self, book_id: int) -> bool:
        """Marca un libro como disponible en el microservicio de libros"""
        try:
            response = requests.post(f"{self.base_url}/api/books/{book_id}/mark_as_available/")
            return response.status_code == 200
        except requests.RequestException:
            return False
