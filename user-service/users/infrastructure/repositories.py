"""
Infrastructure Layer - Repositorios
Implementaciones concretas de los puertos
"""
from typing import List, Optional
from django.db import models
from ..domain.entities import User
from ..domain.ports import UserRepository
from ..models import User as UserModel


class DjangoUserRepository(UserRepository):
    """
    Adaptador - Implementación del repositorio usando Django ORM
    """
    
    def save(self, user: User) -> User:
        """Guardar un usuario"""
        try:
            # Convertir entidad de dominio a modelo Django
            user_data = {
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'created_at': user.created_at,
                'updated_at': user.updated_at
            }
            
            # Crear o actualizar
            django_user, created = UserModel.objects.update_or_create(
                id=user.id,
                defaults=user_data
            )
            
            # Convertir modelo Django a entidad de dominio
            return self._to_domain_entity(django_user)
            
        except Exception as e:
            raise Exception(f"Error al guardar usuario: {str(e)}")

    def find_by_id(self, user_id: str) -> Optional[User]:
        """Buscar usuario por ID"""
        try:
            django_user = UserModel.objects.get(id=user_id)
            return self._to_domain_entity(django_user)
        except UserModel.DoesNotExist:
            return None
        except Exception as e:
            raise Exception(f"Error al buscar usuario por ID: {str(e)}")

    def find_by_email(self, email: str) -> Optional[User]:
        """Buscar usuario por email"""
        try:
            django_user = UserModel.objects.get(email=email)
            return self._to_domain_entity(django_user)
        except UserModel.DoesNotExist:
            return None
        except Exception as e:
            raise Exception(f"Error al buscar usuario por email: {str(e)}")

    def find_all(self) -> List[User]:
        """Obtener todos los usuarios"""
        try:
            django_users = UserModel.objects.all().order_by('-created_at')
            return [self._to_domain_entity(user) for user in django_users]
        except Exception as e:
            raise Exception(f"Error al obtener usuarios: {str(e)}")

    def delete(self, user_id: str) -> bool:
        """Eliminar usuario"""
        try:
            django_user = UserModel.objects.get(id=user_id)
            django_user.delete()
            return True
        except UserModel.DoesNotExist:
            return False
        except Exception as e:
            raise Exception(f"Error al eliminar usuario: {str(e)}")

    def _to_domain_entity(self, django_user: UserModel) -> User:
        """Convertir modelo Django a entidad de dominio"""
        return User(
            id=str(django_user.id),
            name=django_user.name,
            email=django_user.email,
            created_at=django_user.created_at,
            updated_at=django_user.updated_at
        )


