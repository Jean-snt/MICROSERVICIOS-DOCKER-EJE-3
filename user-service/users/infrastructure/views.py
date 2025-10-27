"""
Infrastructure Layer - Views (Controladores)
Manejo de requests HTTP
"""
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from .serializers import UserSerializer, CreateUserSerializer, UpdateUserSerializer
from .repositories import DjangoUserRepository
from .services import EmailService
from ..application.use_cases import (
    CreateUserUseCase,
    GetUserUseCase,
    GetAllUsersUseCase,
    UpdateUserUseCase,
    DeleteUserUseCase
)


# Inicializar dependencias (en una app real, usar inyección de dependencias)
user_repository = DjangoUserRepository()
email_service = EmailService()

create_user_use_case = CreateUserUseCase(user_repository, email_service)
get_user_use_case = GetUserUseCase(user_repository)
get_all_users_use_case = GetAllUsersUseCase(user_repository)
update_user_use_case = UpdateUserUseCase(user_repository)
delete_user_use_case = DeleteUserUseCase(user_repository)


@api_view(['POST'])
def create_user(request):
    """
    Crear un nuevo usuario
    """
    try:
        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            user = create_user_use_case.execute(
                name=serializer.validated_data['name'],
                email=serializer.validated_data['email']
            )
            
            response_serializer = UserSerializer(user)
            return Response({
                'success': True,
                'data': response_serializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'success': False,
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
            
    except ValueError as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({
            'success': False,
            'error': f'Error interno del servidor: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_user(request, user_id):
    """
    Obtener un usuario por ID
    """
    try:
        user = get_user_use_case.execute(user_id)
        serializer = UserSerializer(user)
        return Response({
            'success': True,
            'data': serializer.data
        }, status=status.HTTP_200_OK)
        
    except ValueError as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'success': False,
            'error': f'Error interno del servidor: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_all_users(request):
    """
    Obtener todos los usuarios
    """
    try:
        users = get_all_users_use_case.execute()
        serializer = UserSerializer(users, many=True)
        return Response({
            'success': True,
            'data': serializer.data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'success': False,
            'error': f'Error interno del servidor: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
def update_user(request, user_id):
    """
    Actualizar un usuario
    """
    try:
        serializer = UpdateUserSerializer(data=request.data)
        if serializer.is_valid():
            user = update_user_use_case.execute(
                user_id=user_id,
                name=serializer.validated_data.get('name'),
                email=serializer.validated_data.get('email')
            )
            
            response_serializer = UserSerializer(user)
            return Response({
                'success': True,
                'data': response_serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'success': False,
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
            
    except ValueError as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({
            'success': False,
            'error': f'Error interno del servidor: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
def delete_user(request, user_id):
    """
    Eliminar un usuario
    """
    try:
        success = delete_user_use_case.execute(user_id)
        if success:
            return Response({
                'success': True,
                'message': 'Usuario eliminado correctamente'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'success': False,
                'error': 'Usuario no encontrado'
            }, status=status.HTTP_404_NOT_FOUND)
            
    except ValueError as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({
            'success': False,
            'error': f'Error interno del servidor: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


