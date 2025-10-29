from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, HealthCheckView

router = DefaultRouter()
router.register(r'books', BookViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('health/', HealthCheckView.as_view(), name='health-check'),
]