from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    nome = models.CharField(
        max_length=100, 
        verbose_name='Nome Completo',
        help_text='Nome completo do usuário'
    )
    email = models.EmailField(
        unique=True,
        verbose_name='E-mail',
        help_text='Endereço de e-mail único'
    )
    senha = models.CharField(
        max_length=128,
        verbose_name='Senha',
        help_text='Senha do usuário (será criptografada automaticamente)'
    )
    dt_inclusao = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Data de Inclusão',
        help_text='Data e hora de criação da conta'
    )
    
    USERNAME_FIELD = 'email'  
    REQUIRED_FIELDS = ['username', 'nome'] 
    
    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
        ordering = ['-dt_inclusao']
    
    def __str__(self):
        return f'{self.nome} ({self.email})'
    
    def save(self, *args, **kwargs):
        if self.senha and not self.password:
            self.set_password(self.senha)
        super().save(*args, **kwargs)
