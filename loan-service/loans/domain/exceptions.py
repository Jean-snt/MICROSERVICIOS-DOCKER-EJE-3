"""

loan_microservice/loans/domain/exceptions.py



Define las excepciones personalizadas que se lanzarán cuando se violen las reglas

de negocio dentro de la capa de dominio. Esto garantiza que el dominio sea la única

fuente de verdad para los errores de negocio.

"""



class LoanDomainError(Exception):

    """Clase base para todas las excepciones del dominio de Préstamos."""

    pass



# Excepciones relacionadas con las Reglas de Negocio (3.2)



class MaxActiveLoansReachedError(LoanDomainError):

    """Excepción lanzada cuando el usuario excede el límite de préstamos activos (3)."""

    def __init__(self, user_id: str, limit: int = 3):

        self.user_id = user_id

        self.limit = limit

        super().__init__(f"El usuario {user_id} ha alcanzado el límite de {limit} préstamos activos.")



class UserSuspendedError(LoanDomainError):

    """Excepción lanzada si el usuario está suspendido o inactivo."""

    def __init__(self, user_id: str):

        self.user_id = user_id

        super().__init__(f"El usuario {user_id} está suspendido o inactivo y no puede pedir préstamos.")



class BookUnavailableError(LoanDomainError):

    """Excepción lanzada si el libro no existe, está eliminado o ya está prestado."""

    def __init__(self, book_id: str, reason: str = "no está disponible para préstamo"):

        self.book_id = book_id

        super().__init__(f"El libro {book_id} {reason}.")



class LoanMaxDurationExceededError(LoanDomainError):

    """Excepción lanzada si la duración del préstamo excede el máximo (15 días)."""

    def __init__(self, max_days: int = 15):

        self.max_days = max_days

        super().__init__(f"La duración máxima del préstamo es de {max_days} días.")



# Excepciones de validación de entidad (p.ej., IDs faltantes)



class LoanValidationError(LoanDomainError):

    """Excepción general para errores de validación en la entidad Loan."""

    pass



class LoanNotFoundError(LoanDomainError):

    """Excepción lanzada cuando no se encuentra un préstamo específico."""

    def __init__(self, loan_id: str):

        self.loan_id = loan_id

        super().__init__(f"Préstamo con ID {loan_id} no encontrado.")

