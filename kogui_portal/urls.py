from django.contrib import admin
from django.urls import path, include, re_path
from django.http import JsonResponse
from django.views.generic.base import RedirectView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.views.static import serve
from django.conf import settings

schema_view = get_schema_view(
    openapi.Info(
        title="Kogui Portal API",
        default_version='v1',
        description="API REST para calculadora com autenticação JWT",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contato@koguiportal.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

def api_root(request):
    return JsonResponse({
        'message': 'Bem-vindo à API do Kogui Portal',
        'version': '1.0',
        'documentation': {
            'swagger_ui': '/api/swagger/',
            'redoc': '/api/redoc/',
            'openapi_json': '/api/swagger.json',
            'openapi_yaml': '/api/swagger.yaml'
        },
        'endpoints': {
            'auth': {
                'login': '/api/auth/login/',
                'registro': '/api/auth/registro/',
                'logout': '/api/auth/logout/',
                'perfil': '/api/auth/perfil/',
                'refresh_token': '/api/auth/token/refresh/'
            },
            'calculadora': {
                'calcular': '/api/calc/calcular/',
                'historico': '/api/calc/historico/',
                'operacao_detail': '/api/calc/operacao/{id}/',
                'deletar_operacao': '/api/calc/operacao/{id}/deletar/'
            },
            'admin': '/admin/'
        },
        'authentication': 'JWT Bearer Token required for protected endpoints'
    })

api_urlpatterns = [
    path('auth/', include('autenticacao.urls')),
    path('calc/', include('calculadora.urls')),
]

auth_urlpatterns = [
    path('', include('autenticacao.urls_auth')),
]

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # API
    path('api/', include([
        path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
        path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
        path('', api_root, name='api_root'),
    ] + api_urlpatterns)),

    # Autenticação (não usada no frontend)
    path('auth/', include(auth_urlpatterns)),

    # Redirecionar raiz do site para sua calculadora
    path('', RedirectView.as_view(url='/static/calculadora/index.html', permanent=False)),

    # (opcional) Rotas de fallback direto para arquivos estáticos
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]