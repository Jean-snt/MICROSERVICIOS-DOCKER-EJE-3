"""
CAPA DE INFRAESTRUCTURA - ADAPTADORES DE ENTRADA HTTP
Vistas que exponen la API REST y orquestan los casos de uso
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..application.use_cases import (
    CreateLoanUseCase,
    ReturnLoanUseCase,
    GetLoansByUserUseCase,
    GetAllLoansUseCase,
    GetLoanByIdUseCase
)
from .repositories import DjangoLoanRepository
from .services import HttpUserService, HttpBookService
from .serializers import LoanSerializer, CreateLoanRequestSerializer


class LoanListCreateView(APIView):
    """
    Adaptador de entrada HTTP para listar y crear préstamos
    GET: Lista todos los préstamos
    POST: Crea un nuevo préstamo
    """
    
    def get(self, request):
        """Lista todos los préstamos"""
        # Inyección de dependencias
        repository = DjangoLoanRepository()
        use_case = GetAllLoansUseCase(repository)
        
        # Ejecutar caso de uso
        loans = use_case.execute()
        
        # Serializar respuesta
        loan_data = [LoanSerializer.from_entity(loan) for loan in loans]
        
        return Response({
            'success': True,
            'loans': loan_data
        })
    
    def post(self, request):
        """Crea un nuevo préstamo"""
        # Validar request
        serializer = CreateLoanRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'success': False,
                'error': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Inyección de dependencias (patrón de configuración)
        repository = DjangoLoanRepository()
        user_service = HttpUserService()
        book_service = HttpBookService()
        
        use_case = CreateLoanUseCase(repository, user_service, book_service)
        
        # Ejecutar caso de uso
        result = use_case.execute(
            user_id=serializer.validated_data['user_id'],
            book_id=serializer.validated_data['book_id']
        )
        
        # Responder según resultado
        if result['success']:
            loan_data = LoanSerializer.from_entity(result['loan'])
            return Response({
                'success': True,
                'loan': loan_data,
                'message': result['message']
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'success': False,
                'error': result['error']
            }, status=status.HTTP_400_BAD_REQUEST)


class LoanDetailView(APIView):
    """
    Adaptador de entrada HTTP para operaciones sobre un préstamo específico
    GET: Obtiene detalles de un préstamo
    """
    
    def get(self, request, loan_id):
        """Obtiene un préstamo por ID"""
        repository = DjangoLoanRepository()
        use_case = GetLoanByIdUseCase(repository)
        
        loan = use_case.execute(loan_id)
        
        if loan:
            loan_data = LoanSerializer.from_entity(loan)
            return Response({
                'success': True,
                'loan': loan_data
            })
        else:
            return Response({
                'success': False,
                'error': 'Préstamo no encontrado'
            }, status=status.HTTP_404_NOT_FOUND)


class ReturnLoanView(APIView):
    """
    Adaptador de entrada HTTP para devolver un préstamo
    POST: Marca un préstamo como devuelto
    """
    
    def post(self, request, loan_id):
        """Procesa la devolución de un préstamo"""
        # Inyección de dependencias
        repository = DjangoLoanRepository()
        book_service = HttpBookService()
        
        use_case = ReturnLoanUseCase(repository, book_service)
        
        # Ejecutar caso de uso
        result = use_case.execute(loan_id)
        
        # Responder según resultado
        if result['success']:
            loan_data = LoanSerializer.from_entity(result['loan'])
            return Response({
                'success': True,
                'loan': loan_data,
                'message': result['message']
            })
        else:
            return Response({
                'success': False,
                'error': result['error']
            }, status=status.HTTP_400_BAD_REQUEST)


class UserLoansView(APIView):
    """
    Adaptador de entrada HTTP para obtener préstamos de un usuario
    GET: Lista préstamos de un usuario específico
    """
    
    def get(self, request, user_id):
        """Obtiene préstamos de un usuario"""
        only_active = request.query_params.get('active', 'false').lower() == 'true'
        
        repository = DjangoLoanRepository()
        use_case = GetLoansByUserUseCase(repository)
        
        loans = use_case.execute(user_id, only_active)
        
        loan_data = [LoanSerializer.from_entity(loan) for loan in loans]
        
        return Response({
            'success': True,
            'loans': loan_data,
            'count': len(loan_data)
        })