from abc import ABC, abstractmethod
from typing import List, Optional
from .entities import User, Book, Loan

class UserRepositoryPort(ABC):
    """Puerto para el repositorio de usuarios"""
    
    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[User]:
        """Obtiene un usuario por su ID"""
        pass

class BookRepositoryPort(ABC):
    """Puerto para el repositorio de libros"""
    
    @abstractmethod
    def get_by_id(self, book_id: int) -> Optional[Book]:
        """Obtiene un libro por su ID"""
        pass
    
    @abstractmethod
    def mark_as_loaned(self, book_id: int) -> bool:
        """Marca un libro como prestado"""
        pass
    
    @abstractmethod
    def mark_as_available(self, book_id: int) -> bool:
        """Marca un libro como disponible"""
        pass

class LoanRepositoryPort(ABC):
    """Puerto para el repositorio de préstamos"""
    
    @abstractmethod
    def save(self, loan: Loan) -> Loan:
        """Guarda un préstamo"""
        pass
    
    @abstractmethod
    def get_by_id(self, loan_id: int) -> Optional[Loan]:
        """Obtiene un préstamo por su ID"""
        pass
    
    @abstractmethod
    def get_active_loans_by_user(self, user_id: int) -> List[Loan]:
        """Obtiene todos los préstamos activos de un usuario"""
        pass
    
    @abstractmethod
    def get_all_active_loans(self) -> List[Loan]:
        """Obtiene todos los préstamos activos"""
        pass

class ExternalUserServicePort(ABC):
    """Puerto para el servicio externo de usuarios"""
    
    @abstractmethod
    def get_user(self, user_id: int) -> Optional[User]:
        """Obtiene un usuario del microservicio de usuarios"""
        pass

class ExternalBookServicePort(ABC):
    """Puerto para el servicio externo de libros"""
    
    @abstractmethod
    def get_book(self, book_id: int) -> Optional[Book]:
        """Obtiene un libro del microservicio de libros"""
        pass
    
    @abstractmethod
    def mark_book_as_loaned(self, book_id: int) -> bool:
        """Marca un libro como prestado en el microservicio de libros"""
        pass
    
    @abstractmethod
    def mark_book_as_available(self, book_id: int) -> bool:
        """Marca un libro como disponible en el microservicio de libros"""
        pass
