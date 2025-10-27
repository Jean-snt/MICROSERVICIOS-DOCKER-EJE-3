from django.urls import path
from .views import LoanCreateView

urlpatterns = [
    path('loans/', LoanCreateView.as_view(), name='loan-create'),
]