from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from application.services.loan_service import LoanService
from infrastructure.adapters.db.loan_repository import DjangoLoanRepository
from .serializers import LoanCreationSerializer, LoanResponseSerializer


class LoanCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoanCreationSerializer(data=request.data)
        if serializer.is_valid():
            # Inyección de dependencias
            repo = DjangoLoanRepository()
            service = LoanService(loan_repository=repo)
            try:
                new_loan = service.create_loan(
                    user_id=serializer.validated_data['user_id'],
                    book_id=serializer.validated_data['book_id']
                )
                response_serializer = LoanResponseSerializer(new_loan)
                return Response(response_serializer.data, status=status.HTTP_201_CREATED)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)