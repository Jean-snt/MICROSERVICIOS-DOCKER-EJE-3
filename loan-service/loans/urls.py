"""
URLs del módulo de préstamos
"""
from django.urls import path
from .infrastructure.views import (
    LoanListCreateView,
    LoanDetailView,
    ReturnLoanView,
    UserLoansView
)

urlpatterns = [
    path('loans/', LoanListCreateView.as_view(), name='loan-list-create'),
    path('loans/<int:loan_id>/', LoanDetailView.as_view(), name='loan-detail'),
    path('loans/<int:loan_id>/return/', ReturnLoanView.as_view(), name='loan-return'),
    path('users/<int:user_id>/loans/', UserLoansView.as_view(), name='user-loans'),
]





