from django.contrib import admin
from .models import Operacao


@admin.register(Operacao)
class OperacaoAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'tipo_operacao', 'get_parametros_display', 'resultado', 'data_criacao']
    list_filter = ['tipo_operacao', 'data_criacao', 'usuario']
    search_fields = ['usuario__username', 'usuario__nome']
    readonly_fields = ['data_criacao']
    ordering = ['-data_criacao']
    
    def get_parametros_display(self, obj):
        """Exibe os parâmetros formatados no admin"""
        return obj.get_parametros_display()
    get_parametros_display.short_description = 'Parâmetros'
