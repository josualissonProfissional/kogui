from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

app_name = 'autenticacao'

urlpatterns = [
    path('login/', views.login_api, name='login'),
    path('logout/', views.logout_api, name='logout'),
    path('registro/', views.registro_api, name='registro'),
    path('perfil/', views.perfil_api, name='perfil'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
