from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from adapters.repositories import UserRepositoryAdapter, BookRepositoryAdapter, LoanRepositoryAdapter
from application.loan_use_case import LoanUseCase
from .serializers import LoanSerializer, CreateLoanSerializer, LoanEntitySerializer
from .models import LoanModel

class LoanViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar préstamos usando arquitectura hexagonal"""
    
    serializer_class = LoanSerializer
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Inicializar adaptadores y caso de uso
        self.user_repository = UserRepositoryAdapter()
        self.book_repository = BookRepositoryAdapter()
        self.loan_repository = LoanRepositoryAdapter()
        self.loan_use_case = LoanUseCase(
            self.user_repository,
            self.book_repository,
            self.loan_repository
        )
    
    def get_queryset(self):
        """Obtiene el queryset de préstamos"""
        return LoanModel.objects.all()
    
    def create(self, request):
        """Crea un nuevo préstamo"""
        serializer = CreateLoanSerializer(data=request.data)
        if serializer.is_valid():
            try:
                loan = self.loan_use_case.create_loan(
                    serializer.validated_data['user_id'],
                    serializer.validated_data['book_id']
                )
                # Usar el serializer de entidad para serializar correctamente
                entity_serializer = LoanEntitySerializer(loan)
                return Response(entity_serializer.data, status=status.HTTP_201_CREATED)
            except ValueError as e:
                return Response(
                    {'error': str(e)}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            except Exception as e:
                return Response(
                    {'error': f'Error interno: {str(e)}'}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def return_loan(self, request, pk=None):
        """Devuelve un préstamo"""
        try:
            loan = self.loan_use_case.return_loan(int(pk))
            entity_serializer = LoanEntitySerializer(loan)
            return Response(entity_serializer.data)
        except ValueError as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': f'Error interno: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def user_active_loans(self, request):
        """Obtiene todos los préstamos activos de un usuario"""
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response(
                {'error': 'user_id es requerido'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            loans = self.loan_use_case.get_user_active_loans(int(user_id))
            entity_serializer = LoanEntitySerializer(loans, many=True)
            return Response(entity_serializer.data)
        except ValueError:
            return Response(
                {'error': 'user_id debe ser un número válido'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=False, methods=['get'])
    def active_loans(self, request):
        """Obtiene todos los préstamos activos"""
        loans = self.loan_use_case.get_all_active_loans()
        entity_serializer = LoanEntitySerializer(loans, many=True)
        return Response(entity_serializer.data)
    
    @action(detail=False, methods=['get'])
    def check_user_can_borrow(self, request):
        """Verifica si un usuario puede pedir un préstamo"""
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response(
                {'error': 'user_id es requerido'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            can_borrow, message = self.loan_use_case.check_user_can_borrow(int(user_id))
            return Response({
                'can_borrow': can_borrow,
                'message': message
            })
        except ValueError:
            return Response(
                {'error': 'user_id debe ser un número válido'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=False, methods=['get'])
    def check_book_availability(self, request):
        """Verifica si un libro está disponible para préstamo"""
        book_id = request.query_params.get('book_id')
        if not book_id:
            return Response(
                {'error': 'book_id es requerido'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            is_available, message = self.loan_use_case.check_book_availability(int(book_id))
            return Response({
                'is_available': is_available,
                'message': message
            })
        except ValueError:
            return Response(
                {'error': 'book_id debe ser un número válido'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
