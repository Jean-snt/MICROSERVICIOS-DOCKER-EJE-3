from rest_framework import viewsets, status
from rest_framework.response import Response
from .serializers import LoanSerializer, CreateLoanSerializer
from .dependencies import get_loan_service
from rest_framework.views import APIView


class LoanViewSet(viewsets.ViewSet):
    
    def list(self, request):
        loan_service = get_loan_service()
        loans = loan_service.get_all_loans()
        serializer = LoanSerializer(loans, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = CreateLoanSerializer(data=request.data)
        if serializer.is_valid():
            loan_service = get_loan_service()
            try:
                loan = loan_service.create_loan(
                    user_id=serializer.validated_data['user_id'],
                    book_id=serializer.validated_data['book_id']
                )
                response_serializer = LoanSerializer(loan)
                return Response(response_serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HealthCheckView(APIView):
    def get(self, request):
        return Response({'status': 'ok'}, status=status.HTTP_200_OK)
