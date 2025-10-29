from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LoanViewSet, HealthCheckView

router = DefaultRouter()
router.register(r'loans', LoanViewSet, basename='loan')

urlpatterns = [
    path('', include(router.urls)),
    path('health/', HealthCheckView.as_view(), name='health-check'),
]