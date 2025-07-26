from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import Usuario


class UsuarioSerializer(serializers.ModelSerializer):
    senha = serializers.CharField(
        write_only=True, 
        min_length=8,
        help_text="Senha do usuário (mínimo 8 caracteres)"
    )
    
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'nome', 'email', 'senha', 'dt_inclusao']
        read_only_fields = ['id', 'dt_inclusao']
    
    def create(self, validated_data):
        senha = validated_data.pop('senha')
        usuario = Usuario.objects.create(**validated_data)
        usuario.set_password(senha)
        usuario.senha = senha  
        usuario.save()
        return usuario


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(
        help_text="Endereço de email do usuário"
    )
    senha = serializers.CharField(
        write_only=True,
        help_text="Senha do usuário"
    )
    
    def validate(self, attrs):
        email = attrs.get('email')
        senha = attrs.get('senha')
        
        if email and senha:
            user = authenticate(username=email, password=senha)
            if not user:
                raise serializers.ValidationError('Credenciais inválidas.')
            if not user.is_active:
                raise serializers.ValidationError('Conta desativada.')
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError('Email e senha são obrigatórios.')


class RegistroSerializer(serializers.ModelSerializer):
    senha = serializers.CharField(
        write_only=True, 
        min_length=8,
        help_text="Senha do usuário (mínimo 8 caracteres)"
    )
    confirmar_senha = serializers.CharField(
        write_only=True,
        help_text="Confirmação da senha (deve ser igual à senha)"
    )
    
    class Meta:
        model = Usuario
        fields = ['username', 'nome', 'email', 'senha', 'confirmar_senha']
    
    def validate(self, attrs):
        if attrs['senha'] != attrs['confirmar_senha']:
            raise serializers.ValidationError("As senhas não coincidem.")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('confirmar_senha')
        return UsuarioSerializer().create(validated_data)
