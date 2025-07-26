from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ['username', 'nome', 'email', 'is_active', 'dt_inclusao']
    list_filter = ['is_active', 'is_staff', 'dt_inclusao']
    search_fields = ['username', 'nome', 'email']
    ordering = ['-dt_inclusao']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Informações Adicionais', {
            'fields': ('nome', 'senha', 'dt_inclusao')
        }),
    )
    
    readonly_fields = ['dt_inclusao']
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informações Adicionais', {
            'fields': ('nome', 'email')
        }),
    )
