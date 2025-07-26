from django.views.generic import FormView
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from .forms import RegistroForm

class LoginView(BaseLoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('calculadora:index')
    
    def form_invalid(self, form):
        messages.error(self.request, _("Usuário ou senha inválidos. Por favor, tente novamente."))
        return super().form_invalid(form)


class LogoutView(BaseLogoutView):
    next_page = 'login'
    
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        messages.success(request, _("Você saiu da sua conta com sucesso."))
        return response


class RegistroView(FormView):
    template_name = 'registration/register.html'
    form_class = RegistroForm
    success_url = reverse_lazy('calculadora:index')
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('calculadora:index')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, _("Cadastro realizado com sucesso!"))
        return super().form_valid(form)
    
    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{form.fields[field].label}: {error}")
        return super().form_invalid(form)
