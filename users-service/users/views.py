from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import User
from .serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar usuarios"""
    
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    @action(detail=True, methods=['get'])
    def check_status(self, request, pk=None):
        """Endpoint para verificar el estado de un usuario"""
        user = get_object_or_404(User, pk=pk)
        
        return Response({
            'user_id': user.id,
            'is_active': user.is_active,
            'is_suspended': user.is_suspended,
            'status': user.status
        })
    
    @action(detail=True, methods=['post'])
    def suspend(self, request, pk=None):
        """Endpoint para suspender un usuario"""
        user = get_object_or_404(User, pk=pk)
        user.status = 'suspended'
        user.save()
        
        serializer = self.get_serializer(user)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """Endpoint para activar un usuario"""
        user = get_object_or_404(User, pk=pk)
        user.status = 'active'
        user.save()
        
        serializer = self.get_serializer(user)
        return Response(serializer.data)
