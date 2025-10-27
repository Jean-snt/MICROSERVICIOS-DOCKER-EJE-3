"""
CAPA DE DOMINIO - PUERTOS (INTERFACES)
Definen contratos que deben implementar los adaptadores
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from .entities import LoanEntity, UserEntity, BookEntity


class LoanRepositoryPort(ABC):
    """
    Puerto de salida: Interfaz para el repositorio de préstamos
    Los adaptadores de infraestructura implementarán esta interfaz
    """
    
    @abstractmethod
    def save(self, loan: LoanEntity) -> LoanEntity:
        """Guarda un préstamo en el repositorio"""
        pass
    
    @abstractmethod
    def find_by_id(self, loan_id: int) -> Optional[LoanEntity]:
        """Busca un préstamo por su ID"""
        pass
    
    @abstractmethod
    def find_active_by_user(self, user_id: int) -> List[LoanEntity]:
        """Encuentra todos los préstamos activos de un usuario"""
        pass
    
    @abstractmethod
    def find_by_book(self, book_id: int) -> List[LoanEntity]:
        """Encuentra todos los préstamos de un libro"""
        pass
    
    @abstractmethod
    def find_all(self) -> List[LoanEntity]:
        """Obtiene todos los préstamos"""
        pass
    
    @abstractmethod
    def update(self, loan: LoanEntity) -> LoanEntity:
        """Actualiza un préstamo existente"""
        pass


class UserServicePort(ABC):
    """
    Puerto de salida: Interfaz para comunicación con el servicio de usuarios
    """
    
    @abstractmethod
    def get_user(self, user_id: int) -> Optional[UserEntity]:
        """Obtiene información de un usuario"""
        pass
    
    @abstractmethod
    def verify_user_exists(self, user_id: int) -> bool:
        """Verifica si un usuario existe"""
        pass


class BookServicePort(ABC):
    """
    Puerto de salida: Interfaz para comunicación con el servicio de libros
    """
    
    @abstractmethod
    def get_book(self, book_id: int) -> Optional[BookEntity]:
        """Obtiene información de un libro"""
        pass
    
    @abstractmethod
    def verify_book_availability(self, book_id: int) -> bool:
        """Verifica si un libro está disponible"""
        pass
    
    @abstractmethod
    def mark_book_as_loaned(self, book_id: int) -> bool:
        """Marca un libro como prestado"""
        pass
    
    @abstractmethod
    def mark_book_as_available(self, book_id: int) -> bool:
        """Marca un libro como disponible"""
        pass



