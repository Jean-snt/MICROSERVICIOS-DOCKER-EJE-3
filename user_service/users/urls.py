from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, HealthCheckView

router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('health/', HealthCheckView.as_view(), name='health-check'),
]