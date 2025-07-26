from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import UsuarioSerializer, LoginSerializer, RegistroSerializer

@swagger_auto_schema(
    method='post',
    operation_summary="Login de usuário",
    operation_description="Autentica um usuário e retorna tokens JWT para acesso à API",
    request_body=LoginSerializer,
    responses={
        200: openapi.Response(
            description="Login realizado com sucesso",
            examples={
                "application/json": {
                    "message": "Login realizado com sucesso",
                    "user": {
                        "id": 1,
                        "username": "joao123",
                        "nome": "João Silva",
                        "email": "joao@email.com"
                    },
                    "tokens": {
                        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
                    }
                }
            }
        ),
        400: openapi.Response(
            description="Credenciais inválidas",
            examples={
                "application/json": {
                    "error": "Credenciais inválidas",
                    "details": {"email": ["Este campo é obrigatório."]}
                }
            }
        )
    },
    tags=['Autenticação']
)
@api_view(['POST'])
@permission_classes([AllowAny])
def login_api(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'message': 'Login realizado com sucesso',
            'user': {
                'id': user.id,
                'username': user.username,
                'nome': user.nome,
                'email': user.email
            },
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_200_OK)
    
    return Response({
        'error': 'Credenciais inválidas',
        'details': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='post',
    operation_summary="Registro de novo usuário",
    operation_description="Cria uma nova conta de usuário e retorna tokens JWT",
    request_body=RegistroSerializer,
    responses={
        201: openapi.Response(
            description="Usuário criado com sucesso",
            examples={
                "application/json": {
                    "message": "Usuário criado com sucesso",
                    "user": {
                        "id": 1,
                        "username": "joao123",
                        "nome": "João Silva",
                        "email": "joao@email.com"
                    },
                    "tokens": {
                        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
                    }
                }
            }
        ),
        400: openapi.Response(
            description="Erro na validação dos dados",
            examples={
                "application/json": {
                    "error": "Erro ao criar usuário",
                    "details": {"email": ["Usuário com este E-mail já existe."]}
                }
            }
        )
    },
    tags=['Autenticação']
)
@api_view(['POST'])
@permission_classes([AllowAny])
def registro_api(request):
    serializer = RegistroSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'message': 'Usuário criado com sucesso',
            'user': {
                'id': user.id,
                'username': user.username,
                'nome': user.nome,
                'email': user.email
            },
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)
    
    return Response({
        'error': 'Erro ao criar usuário',
        'details': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='post',
    operation_summary="Logout de usuário",
    operation_description="Invalida o refresh token do usuário (blacklist)",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'refresh': openapi.Schema(type=openapi.TYPE_STRING, description='Refresh token JWT')
        },
        required=['refresh']
    ),
    responses={
        200: openapi.Response(
            description="Logout realizado com sucesso",
            examples={
                "application/json": {
                    "message": "Logout realizado com sucesso"
                }
            }
        ),
        400: openapi.Response(
            description="Token inválido",
            examples={
                "application/json": {
                    "error": "Token de refresh inválido ou faltando"
                }
            }
        )
    },
    tags=['Autenticação']
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_api(request):
    try:
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response(
                {'error': 'Token de refresh é obrigatório'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        token = RefreshToken(refresh_token)
        token.blacklist()
        
        return Response({
            'message': 'Logout realizado com sucesso'
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'error': 'Erro ao fazer logout',
            'details': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='get',
    operation_summary="Perfil do usuário",
    operation_description="Retorna os dados do usuário autenticado",
    responses={
        200: UsuarioSerializer,
        401: openapi.Response(
            description="Token inválido ou ausente",
            examples={
                "application/json": {
                    "detail": "As credenciais de autenticação não foram fornecidas."
                }
            }
        )
    },
    tags=['Autenticação']
)
@api_view(['GET'])
def perfil_api(request):
    serializer = UsuarioSerializer(request.user)
    return Response(serializer.data)
