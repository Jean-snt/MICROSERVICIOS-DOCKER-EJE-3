"""
URLs del módulo de usuarios
"""
from django.urls import path
from .views import (
    UserListCreateView,
    UserDetailView,
    SuspendUserView,
    UnsuspendUserView,
    ActiveUsersView
)

urlpatterns = [
    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:user_id>/', UserDetailView.as_view(), name='user-detail'),
    path('users/<int:user_id>/suspend/', SuspendUserView.as_view(), name='user-suspend'),
    path('users/<int:user_id>/unsuspend/', UnsuspendUserView.as_view(), name='user-unsuspend'),
    path('users/active/', ActiveUsersView.as_view(), name='user-active'),
]
