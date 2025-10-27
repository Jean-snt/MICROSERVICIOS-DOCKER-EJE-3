"""
CAPA DE APLICACIÓN - CASOS DE USO
Orquesta la lógica de negocio sin depender de detalles de implementación
"""
from typing import Optional, List, Dict, Any
from ..domain.entities import LoanEntity, UserEntity, BookEntity
from ..domain.ports import LoanRepositoryPort, UserServicePort, BookServicePort


class CreateLoanUseCase:
    """
    Caso de uso: Crear un nuevo préstamo
    Implementa todas las reglas de negocio del flujo de préstamos
    """
    
    # Constante de regla de negocio
    MAX_ACTIVE_LOANS_PER_USER = 3
    
    def __init__(
        self,
        loan_repository: LoanRepositoryPort,
        user_service: UserServicePort,
        book_service: BookServicePort
    ):
        self.loan_repository = loan_repository
        self.user_service = user_service
        self.book_service = book_service
    
    def execute(self, user_id: int, book_id: int) -> Dict[str, Any]:
        """
        Ejecuta el caso de uso de creación de préstamo
        
        Returns:
            Dict con 'success', 'loan' (si exitoso) o 'error' (si falla)
        """
        # 1. Validar que el usuario existe y está activo
        user = self.user_service.get_user(user_id)
        if not user:
            return {'success': False, 'error': 'Usuario no encontrado'}
        
        can_loan, error_msg = user.can_request_loan()
        if not can_loan:
            return {'success': False, 'error': error_msg}
        
        # 2. Validar límite de préstamos activos (Regla de negocio)
        active_loans = self.loan_repository.find_active_by_user(user_id)
        if len(active_loans) >= self.MAX_ACTIVE_LOANS_PER_USER:
            return {
                'success': False,
                'error': f'Usuario ha alcanzado el límite de {self.MAX_ACTIVE_LOANS_PER_USER} préstamos activos'
            }
        
        # 3. Verificar que el libro existe y está disponible
        book = self.book_service.get_book(book_id)
        if not book:
            return {'success': False, 'error': 'Libro no encontrado'}
        
        can_be_loaned, error_msg = book.can_be_loaned()
        if not can_be_loaned:
            return {'success': False, 'error': error_msg}
        
        # 4. Crear la entidad de préstamo (aplica regla de 15 días)
        loan_entity = LoanEntity.create_new_loan(user_id, book_id)
        
        # 5. Validar la entidad
        is_valid, validation_error = loan_entity.validate()
        if not is_valid:
            return {'success': False, 'error': validation_error}
        
        # 6. Guardar el préstamo
        saved_loan = self.loan_repository.save(loan_entity)
        
        # 7. Actualizar estado del libro a "prestado"
        book_updated = self.book_service.mark_book_as_loaned(book_id)
        if not book_updated:
            # En un sistema real, aquí implementaríamos compensación
            return {
                'success': False,
                'error': 'Error al actualizar estado del libro'
            }
        
        return {
            'success': True,
            'loan': saved_loan,
            'message': 'Préstamo creado exitosamente'
        }


class ReturnLoanUseCase:
    """
    Caso de uso: Devolver un préstamo
    """
    
    def __init__(
        self,
        loan_repository: LoanRepositoryPort,
        book_service: BookServicePort
    ):
        self.loan_repository = loan_repository
        self.book_service = book_service
    
    def execute(self, loan_id: int) -> Dict[str, Any]:
        """
        Ejecuta el caso de uso de devolución de préstamo
        """
        # 1. Buscar el préstamo
        loan = self.loan_repository.find_by_id(loan_id)
        if not loan:
            return {'success': False, 'error': 'Préstamo no encontrado'}
        
        # 2. Verificar que el préstamo está activo
        if loan.status != 'active':
            return {'success': False, 'error': 'El préstamo ya fue devuelto'}
        
        # 3. Marcar préstamo como devuelto (lógica de dominio)
        loan.mark_as_returned()
        
        # 4. Actualizar el préstamo
        updated_loan = self.loan_repository.update(loan)
        
        # 5. Marcar libro como disponible
        book_updated = self.book_service.mark_book_as_available(loan.book_id)
        if not book_updated:
            return {
                'success': False,
                'error': 'Préstamo devuelto pero error al actualizar libro'
            }
        
        return {
            'success': True,
            'loan': updated_loan,
            'message': 'Préstamo devuelto exitosamente'
        }


class GetLoansByUserUseCase:
    """
    Caso de uso: Obtener préstamos de un usuario
    """
    
    def __init__(self, loan_repository: LoanRepositoryPort):
        self.loan_repository = loan_repository
    
    def execute(self, user_id: int, only_active: bool = False) -> List[LoanEntity]:
        """Obtiene los préstamos de un usuario"""
        if only_active:
            return self.loan_repository.find_active_by_user(user_id)
        else:
            # En un repositorio real, tendríamos un método para esto
            all_loans = self.loan_repository.find_all()
            return [loan for loan in all_loans if loan.user_id == user_id]


class GetAllLoansUseCase:
    """
    Caso de uso: Obtener todos los préstamos
    """
    
    def __init__(self, loan_repository: LoanRepositoryPort):
        self.loan_repository = loan_repository
    
    def execute(self) -> List[LoanEntity]:
        """Obtiene todos los préstamos"""
        return self.loan_repository.find_all()


class GetLoanByIdUseCase:
    """
    Caso de uso: Obtener un préstamo por ID
    """
    
    def __init__(self, loan_repository: LoanRepositoryPort):
        self.loan_repository = loan_repository
    
    def execute(self, loan_id: int) -> Optional[LoanEntity]:
        """Obtiene un préstamo por su ID"""
        return self.loan_repository.find_by_id(loan_id)



