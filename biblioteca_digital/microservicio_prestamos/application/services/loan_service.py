from datetime import date, timedelta
from domain.models.loan import Loan
from domain.ports import LoanRepositoryPort

class LoanService:
    """
    Contiene la lógica de los casos de uso para los préstamos.
    Orquesta el dominio y depende de los puertos para la infraestructura.
    """
    def __init__(self, loan_repository: LoanRepositoryPort):
        """
        El servicio recibe el adaptador de repositorio a través de
        inyección de dependencias.
        """
        self.loan_repository = loan_repository

    def create_loan(self, user_id: int, book_id: int) -> Loan:
        """
        Caso de uso para crear un nuevo préstamo.
        Aplica las reglas de negocio.
        """
        # Regla de negocio: Límite de 3 préstamos activos por usuario
        active_loans = self.loan_repository.find_active_by_user_id(user_id)
        if len(active_loans) >= 3:
            raise ValueError("El usuario ha alcanzado el límite de préstamos activos.")

        # Regla de negocio: Duración máxima de préstamo: 15 días
        start_date = date.today()
        due_date = start_date + timedelta(days=15)

        new_loan = Loan(
            id=None,
            user_id=user_id,
            book_id=book_id,
            loan_date=start_date,
            due_date=due_date,
            status="activo"
        )

        # Persistir a través del puerto
        return self.loan_repository.save(new_loan)