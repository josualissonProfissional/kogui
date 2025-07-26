from django.db import models
from django.conf import settings
import json

class Operacao(models.Model):
    TIPOS_OPERACAO = [
        ('soma', 'Soma'),
        ('subtracao', 'Subtração'),
        ('multiplicacao', 'Multiplicação'),
        ('divisao', 'Divisão'),
    ]
    
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Usuário')
    tipo_operacao = models.CharField(max_length=20, choices=TIPOS_OPERACAO, verbose_name='Tipo de Operação')
    parametros = models.TextField(verbose_name='Parâmetros')
    resultado = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Resultado')
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')
    
    class Meta:
        verbose_name = 'Operação'
        verbose_name_plural = 'Operações'
        ordering = ['-data_criacao']
    
    def __str__(self):
        params = self.get_parametros_list()
        if len(params) >= 2:
            return f'{self.usuario.username} - {params[0]} {self.get_simbolo_operacao()} {params[1]} = {self.resultado}'
        return f'{self.usuario.username} - {self.tipo_operacao}({params}) = {self.resultado}'
    
    def get_simbolo_operacao(self):
        simbolos = {
            'soma': '+',
            'subtracao': '-',
            'multiplicacao': '×',
            'divisao': '÷'
        }
        return simbolos.get(self.tipo_operacao, '?')
    
    def get_parametros_list(self):
        try:
            return json.loads(self.parametros)
        except (json.JSONDecodeError, TypeError):
            return []
    
    def set_parametros_list(self, parametros_list):
        self.parametros = json.dumps(parametros_list)
    
    def get_parametros_display(self):
        params = self.get_parametros_list()
        return ', '.join(map(str, params))
    
    @staticmethod
    def get_simbolo_operacao_by_tipo(tipo):
        simbolos = {
            'soma': '+',
            'subtracao': '-',
            'multiplicacao': '×',
            'divisao': '÷'
        }
        return simbolos.get(tipo, '?')
