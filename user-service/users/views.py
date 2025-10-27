"""
Vistas para el microservicio de usuarios
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import User
from .serializers import UserSerializer, UserListSerializer, CreateUserSerializer


class UserListCreateView(APIView):
    """
    GET: Lista todos los usuarios
    POST: Crea un nuevo usuario
    """
    
    def get(self, request):
        """Lista usuarios activos"""
        include_inactive = request.query_params.get('include_inactive', 'false').lower() == 'true'
        
        if include_inactive:
            users = User.objects.all()
        else:
            users = User.objects.filter(is_active=True)
        
        serializer = UserListSerializer(users, many=True)
        
        return Response({
            'success': True,
            'users': serializer.data,
            'count': len(serializer.data)
        })
    
    def post(self, request):
        """Crea un nuevo usuario"""
        serializer = CreateUserSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            full_serializer = UserSerializer(user)
            return Response({
                'success': True,
                'user': full_serializer.data,
                'message': 'Usuario creado exitosamente'
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'success': False,
            'error': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(APIView):
    """
    GET: Obtiene detalles de un usuario
    PUT: Actualiza un usuario
    DELETE: Desactiva un usuario
    """
    
    def get(self, request, user_id):
        """Obtiene un usuario por ID"""
        user = get_object_or_404(User, id=user_id)
        serializer = UserSerializer(user)
        
        return Response({
            'success': True,
            'user': serializer.data
        })
    
    def put(self, request, user_id):
        """Actualiza un usuario"""
        user = get_object_or_404(User, id=user_id)
        serializer = UserSerializer(user, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'user': serializer.data,
                'message': 'Usuario actualizado exitosamente'
            })
        
        return Response({
            'success': False,
            'error': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, user_id):
        """Desactiva un usuario (soft delete)"""
        user = get_object_or_404(User, id=user_id)
        user.is_active = False
        user.save()
        
        return Response({
            'success': True,
            'message': 'Usuario desactivado exitosamente'
        })


class SuspendUserView(APIView):
    """
    POST: Suspende un usuario
    """
    
    def post(self, request, user_id):
        """Suspende un usuario"""
        user = get_object_or_404(User, id=user_id)
        
        reason = request.data.get('reason', '')
        
        user.is_suspended = True
        user.suspension_reason = reason
        user.save()
        
        return Response({
            'success': True,
            'message': 'Usuario suspendido exitosamente'
        })


class UnsuspendUserView(APIView):
    """
    POST: Quita la suspensión de un usuario
    """
    
    def post(self, request, user_id):
        """Quita la suspensión de un usuario"""
        user = get_object_or_404(User, id=user_id)
        
        user.is_suspended = False
        user.suspension_reason = ''
        user.save()
        
        return Response({
            'success': True,
            'message': 'Suspensión del usuario removida exitosamente'
        })


class ActiveUsersView(APIView):
    """
    GET: Lista usuarios activos y no suspendidos
    """
    
    def get(self, request):
        """Lista usuarios que pueden solicitar préstamos"""
        users = User.objects.filter(is_active=True, is_suspended=False)
        serializer = UserListSerializer(users, many=True)
        
        return Response({
            'success': True,
            'users': serializer.data,
            'count': len(serializer.data)
        })





