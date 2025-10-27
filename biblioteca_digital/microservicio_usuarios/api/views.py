from rest_framework import generics
from .models import User
from .serializers import UserSerializer

class UserListCreateView(generics.ListCreateAPIView):
    """
    Vista para listar todos los usuarios y crear un nuevo usuario.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
