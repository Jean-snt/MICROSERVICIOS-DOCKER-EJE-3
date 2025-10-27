"""
Domain Layer - Ports (Interfaces)
Define los contratos para la capa de infraestructura
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from .entities import User


class UserRepository(ABC):
    """
    Port - Define el contrato para el repositorio de usuarios
    """
    
    @abstractmethod
    def save(self, user: User) -> User:
        """Guardar un usuario"""
        pass
    
    @abstractmethod
    def find_by_id(self, user_id: str) -> Optional[User]:
        """Buscar usuario por ID"""
        pass
    
    @abstractmethod
    def find_by_email(self, email: str) -> Optional[User]:
        """Buscar usuario por email"""
        pass
    
    @abstractmethod
    def find_all(self) -> List[User]:
        """Obtener todos los usuarios"""
        pass
    
    @abstractmethod
    def delete(self, user_id: str) -> bool:
        """Eliminar usuario"""
        pass


class UserService(ABC):
    """
    Port - Define el contrato para servicios externos
    """
    
    @abstractmethod
    def send_welcome_email(self, user: User) -> bool:
        """Enviar email de bienvenida"""
        pass

