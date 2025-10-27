"""
Application Layer - Casos de uso
Contiene la lógica de aplicación y orquestación
"""
from typing import List, Optional
from ..domain.entities import User
from ..domain.ports import UserRepository, UserService


class CreateUserUseCase:
    """
    Caso de uso para crear un usuario
    """
    
    def __init__(self, user_repository: UserRepository, user_service: UserService = None):
        self.user_repository = user_repository
        self.user_service = user_service

    def execute(self, name: str, email: str) -> User:
        """
        Ejecutar el caso de uso de crear usuario
        """
        # Verificar si el usuario ya existe
        existing_user = self.user_repository.find_by_email(email)
        if existing_user:
            raise ValueError(f"Ya existe un usuario con el email: {email}")

        # Crear nueva entidad de usuario
        user = User.create(name, email)

        # Guardar en el repositorio
        saved_user = self.user_repository.save(user)

        # Enviar email de bienvenida (opcional)
        if self.user_service:
            try:
                self.user_service.send_welcome_email(saved_user)
            except Exception as e:
                # Log el error pero no fallar la creación del usuario
                print(f"Error enviando email de bienvenida: {e}")

        return saved_user


class GetUserUseCase:
    """
    Caso de uso para obtener un usuario por ID
    """
    
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, user_id: str) -> User:
        """
        Ejecutar el caso de uso de obtener usuario
        """
        if not user_id:
            raise ValueError("El ID del usuario es requerido")

        user = self.user_repository.find_by_id(user_id)
        if not user:
            raise ValueError(f"Usuario con ID {user_id} no encontrado")

        return user


class GetAllUsersUseCase:
    """
    Caso de uso para obtener todos los usuarios
    """
    
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self) -> List[User]:
        """
        Ejecutar el caso de uso de obtener todos los usuarios
        """
        return self.user_repository.find_all()


class UpdateUserUseCase:
    """
    Caso de uso para actualizar un usuario
    """
    
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, user_id: str, name: str = None, email: str = None) -> User:
        """
        Ejecutar el caso de uso de actualizar usuario
        """
        if not user_id:
            raise ValueError("El ID del usuario es requerido")

        user = self.user_repository.find_by_id(user_id)
        if not user:
            raise ValueError(f"Usuario con ID {user_id} no encontrado")

        # Actualizar campos si se proporcionan
        if name is not None:
            user.update_name(name)
        
        if email is not None:
            # Verificar que el nuevo email no esté en uso
            existing_user = self.user_repository.find_by_email(email)
            if existing_user and existing_user.id != user_id:
                raise ValueError(f"Ya existe un usuario con el email: {email}")
            user.update_email(email)

        return self.user_repository.save(user)


class DeleteUserUseCase:
    """
    Caso de uso para eliminar un usuario
    """
    
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, user_id: str) -> bool:
        """
        Ejecutar el caso de uso de eliminar usuario
        """
        if not user_id:
            raise ValueError("El ID del usuario es requerido")

        user = self.user_repository.find_by_id(user_id)
        if not user:
            raise ValueError(f"Usuario con ID {user_id} no encontrado")

        return self.user_repository.delete(user_id)


