from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Operacao
from .serializers import OperacaoSerializer
import json

class OperacaoPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['numeros', 'tipo_operacao'],
        properties={
            'numeros': openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(type=openapi.TYPE_NUMBER),
                example=[10.5, 20.3, 5.2]
            ),
            'tipo_operacao': openapi.Schema(
                type=openapi.TYPE_STRING,
                enum=['soma', 'subtracao', 'multiplicacao', 'divisao'],
                example='soma'
            )
        }
    ),
    responses={
        201: openapi.Response(
            description="Operação realizada com sucesso",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(type=openapi.TYPE_STRING),
                    'operacao': openapi.Schema(type=openapi.TYPE_OBJECT)
                }
            )
        ),
        400: openapi.Response(
            description="Requisição inválida",
            examples={
                "application/json": {"error": "Mensagem de erro"}
            }
        ),
        401: openapi.Response(
            description="Não autenticado",
            examples={"application/json": {"detail": "Credenciais não fornecidas."}}
        )
    },
    tags=['Calculadora']
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def calcular_api(request):
    try:
        data = request.data
        
        if 'numeros' in data and isinstance(data['numeros'], list) and len(data['numeros']) >= 2:
            numeros = [float(n) for n in data['numeros']]
        elif 'parametros' in data and isinstance(data['parametros'], list):
            numeros = [float(n) for n in data['parametros']]
        else:
            return Response(
                {'error': 'Envie uma lista de números válida com pelo menos 2 valores.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        tipo_operacao = data.get('tipo_operacao')
        
        if not tipo_operacao or tipo_operacao not in ['soma', 'subtracao', 'multiplicacao', 'divisao']:
            return Response(
                {'error': 'Tipo de operação inválido'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if tipo_operacao == 'soma':
            resultado = sum(numeros)
        elif tipo_operacao == 'subtracao':
            resultado = numeros[0]
            for num in numeros[1:]:
                resultado -= num
        elif tipo_operacao == 'multiplicacao':
            resultado = 1
            for num in numeros:
                resultado *= num
        elif tipo_operacao == 'divisao':
            if 0 in numeros[1:]:
                return Response({
                    'error': 'Divisão por zero não é permitida'
                }, status=status.HTTP_400_BAD_REQUEST)
            resultado = numeros[0]
            for num in numeros[1:]:
                resultado /= num
        
        operacao = Operacao.objects.create(
            usuario=request.user,
            tipo_operacao=tipo_operacao,
            parametros=json.dumps(numeros),
            resultado=resultado
        )
        
        from .serializers import OperacaoSerializer
        serializer = OperacaoSerializer(operacao)
        
        return Response({
            'message': 'Cálculo realizado com sucesso',
            'operacao': serializer.data
        }, status=status.HTTP_201_CREATED)
            
    except Exception as e:
        return Response(
            {'error': f'Erro inesperado: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter(
            'page', openapi.IN_QUERY,
            type=openapi.TYPE_INTEGER,
            default=1
        ),
        openapi.Parameter(
            'page_size', openapi.IN_QUERY,
            type=openapi.TYPE_INTEGER,
            default=10
        )
    ],
    responses={
        200: openapi.Response(
            description="Lista de operações paginada",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'count': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'next': openapi.Schema(type=openapi.TYPE_STRING),
                    'previous': openapi.Schema(type=openapi.TYPE_STRING),
                    'results': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(type=openapi.TYPE_OBJECT)
                    )
                }
            )
        ),
        401: openapi.Response(description="Não autenticado")
    },
    tags=['Calculadora']
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def historico_api(request):
    operacoes = Operacao.objects.filter(usuario=request.user).order_by('-data_criacao')
    paginator = OperacaoPagination()
    page = paginator.paginate_queryset(operacoes, request)
    
    if page is not None:
        serializer = OperacaoSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    serializer = OperacaoSerializer(operacoes, many=True)
    return Response(serializer.data)


@swagger_auto_schema(
    method='get',
    responses={
        200: openapi.Response(
            description="Detalhes da operação",
            schema=OperacaoSerializer()
        ),
        404: openapi.Response(
            description="Operação não encontrada",
            examples={"application/json": {"error": "Operação não encontrada"}}
        ),
        401: openapi.Response(description="Não autenticado")
    },
    tags=['Calculadora']
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def operacao_detail_api(request, pk):
    try:
        operacao = Operacao.objects.get(pk=pk, usuario=request.user)
        serializer = OperacaoSerializer(operacao)
        return Response(serializer.data)
    except Operacao.DoesNotExist:
        return Response(
            {'error': 'Operação não encontrada'},
            status=status.HTTP_404_NOT_FOUND
        )

@swagger_auto_schema(
    method='delete',
    responses={
        200: openapi.Response(
            description="Operação deletada com sucesso",
            examples={"application/json": {"message": "Operação deletada com sucesso"}}
        ),
        404: openapi.Response(
            description="Operação não encontrada",
            examples={"application/json": {"error": "Operação não encontrada"}}
        ),
        401: openapi.Response(description="Não autenticado")
    },
    tags=['Calculadora']
)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deletar_operacao_api(request, pk):
    try:
        operacao = Operacao.objects.get(pk=pk, usuario=request.user)
        operacao.delete()
        return Response(
            {'message': 'Operação deletada com sucesso'},
            status=status.HTTP_200_OK
        )
    except Operacao.DoesNotExist:
        return Response(
            {'error': 'Operação não encontrada'},
            status=status.HTTP_404_NOT_FOUND
        )

@swagger_auto_schema(
    method='delete',
    responses={
        200: openapi.Response(
            description="Todas as operações foram deletadas com sucesso",
            examples={"application/json": {"message": "Todas as operações foram deletadas com sucesso", "count": 5}}
        ),
        401: openapi.Response(description="Não autenticado")
    },
    tags=['Calculadora']
)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def limpar_historico_api(request):
    try:
        count = Operacao.objects.filter(usuario=request.user).count()
        
        Operacao.objects.filter(usuario=request.user).delete()
        
        return Response(
            {
                'message': 'Todas as operações foram deletadas com sucesso',
                'count': count
            },
            status=status.HTTP_200_OK
        )
    except Exception as e:
        return Response(
            {'error': f'Erro ao limpar o histórico: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
