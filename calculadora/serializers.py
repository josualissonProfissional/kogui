from rest_framework import serializers
from .models import Operacao
import json


class OperacaoSerializer(serializers.ModelSerializer):
    usuario_nome = serializers.CharField(
        source='usuario.nome', 
        read_only=True
    )
    parametros_display = serializers.CharField(
        source='get_parametros_display',
        read_only=True
    )
    simbolo_operacao = serializers.CharField(
        source='get_simbolo_operacao', 
        read_only=True
    )
    
    resultado_serializado = serializers.DecimalField(
        source='resultado',
        max_digits=10,
        decimal_places=2,
        coerce_to_string=False,
        read_only=True
    )
    
    class Meta:
        model = Operacao
        fields = [
            'id', 'usuario', 'usuario_nome', 'tipo_operacao', 
            'parametros', 'parametros_display', 'resultado_serializado', 'data_criacao', 'simbolo_operacao'
        ]
        read_only_fields = ['id', 'usuario', 'resultado', 'data_criacao']
    
    def create(self, validated_data):
        parametros_str = validated_data['parametros']
        tipo_operacao = validated_data['tipo_operacao']
        
        try:
            parametros = json.loads(parametros_str)
            parametros = [float(p) for p in parametros]
        except (json.JSONDecodeError, ValueError, TypeError):
            raise serializers.ValidationError("Parâmetros devem ser uma lista de números em formato JSON válido.")
        
        if len(parametros) < 2:
            raise serializers.ValidationError("São necessários pelo menos 2 parâmetros para a operação.")
        
        try:
            if tipo_operacao == 'soma':
                resultado = sum(parametros)
            elif tipo_operacao == 'subtracao':
                resultado = parametros[0]
                for num in parametros[1:]:
                    resultado -= num
            elif tipo_operacao == 'multiplicacao':
                resultado = 1
                for num in parametros:
                    resultado *= num
            elif tipo_operacao == 'divisao':
                if 0 in parametros[1:]:
                    raise serializers.ValidationError("Divisão por zero não é permitida.")
                resultado = parametros[0]
                for num in parametros[1:]:
                    resultado /= num
            else:
                raise serializers.ValidationError("Tipo de operação inválido.")
                
        except Exception as e:
            raise serializers.ValidationError(f"Erro ao realizar operação: {str(e)}")
            
        operacao = Operacao.objects.create(
            usuario=self.context['request'].user,
            tipo_operacao=tipo_operacao,
            parametros=parametros_str,
            resultado=resultado
        )
        return operacao


class CalcularSerializer(serializers.Serializer):
    parametros = serializers.ListField(
        child=serializers.DecimalField(max_digits=10, decimal_places=2),
        min_length=2
    )
    tipo_operacao = serializers.ChoiceField(choices=Operacao.TIPOS_OPERACAO)
    
    def validate(self, attrs):
        parametros = attrs['parametros']
        tipo_operacao = attrs['tipo_operacao']
        
        if not all(isinstance(p, (int, float)) for p in parametros):
            raise serializers.ValidationError("Todos os parâmetros devem ser números válidos.")
        
        if tipo_operacao == 'divisao' and len(parametros) > 1 and parametros[1] == 0:
            raise serializers.ValidationError("Divisão por zero não é permitida.")
        
        return attrs
