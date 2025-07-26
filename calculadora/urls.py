from django.urls import path
from . import views

app_name = 'calculadora'

urlpatterns = [
    path('calcular/', views.calcular_api, name='calcular'),
    path('historico/', views.historico_api, name='historico'),
    path('operacao/<int:pk>/', views.operacao_detail_api, name='operacao_detail'),
    path('operacao/<int:pk>/deletar/', views.deletar_operacao_api, name='deletar_operacao'),
    path('limpar_historico/', views.limpar_historico_api, name='limpar_historico'),
]
