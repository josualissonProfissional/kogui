from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views_auth

app_name = 'autenticacao'

urlpatterns = [
    # URLs de autenticação baseadas em classes
    path('login/', 
         auth_views.LoginView.as_view(
             template_name='registration/login.html',
             redirect_authenticated_user=True,
             next_page=reverse_lazy('calculadora:index')
         ), 
         name='login'),
         
    path('logout/', 
         auth_views.LogoutView.as_view(
             next_page=reverse_lazy('autenticacao:login')
         ), 
         name='logout'),
         
    path('registro/', 
         views_auth.RegistroView.as_view(), 
         name='registro'),
         
    # Redirecionamentos para manter compatibilidade
    path('entrar/', lambda request: redirect('autenticacao:login'), name='entrar'),
    path('sair/', lambda request: redirect('autenticacao:logout'), name='sair'),
    path('cadastro/', lambda request: redirect('autenticacao:registro'), name='cadastro'),
]
