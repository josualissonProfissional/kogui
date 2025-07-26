from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from .models import Usuario

class RegistroForm(UserCreationForm):
    email = forms.EmailField(
        label=_('E-mail'),
        max_length=254,
        help_text=_('Informe um endereço de e-mail válido.'),
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': _('seu@email.com'),
            'autocomplete': 'email',
            'required': 'required'
        })
    )
    
    nome = forms.CharField(
        label=_('Nome Completo'),
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Seu nome completo'),
            'autocomplete': 'name',
            'required': 'required'
        })
    )
    
    password1 = forms.CharField(
        label=_('Senha'),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _('Digite uma senha forte'),
            'autocomplete': 'new-password',
            'required': 'required'
        }),
        help_text=_(
            'Sua senha deve conter pelo menos 8 caracteres, incluindo letras e números.'
        ),
    )
    
    password2 = forms.CharField(
        label=_('Confirmação de Senha'),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _('Digite a senha novamente'),
            'autocomplete': 'new-password',
            'required': 'required'
        }),
        help_text=_('Digite a mesma senha novamente para verificação.'),
    )
    
    class Meta:
        model = Usuario
        fields = ('username', 'email', 'nome', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Escolha um nome de usuário'),
                'autocomplete': 'username',
                'required': 'required'
            }),
        }
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError(_('Este e-mail já está em uso.'))
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if Usuario.objects.filter(username=username).exists():
            raise forms.ValidationError(_('Este nome de usuário já está em uso.'))
        return username
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.nome = self.cleaned_data['nome']
        user.senha = self.cleaned_data['password1'] 
        if commit:
            user.save()
        return user
