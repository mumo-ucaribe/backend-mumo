from rest_framework import serializers
from .models import User, Insumo, Receta, Venta, Merma

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    
class insumoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Insumo
        fields = ['id', 'nombre', 'cantidad', 'unidad', 'precio_unitario', 'fecha_creacion']
        read_only_fields = ['id', 'fecha_creacion']
        extra_kwargs = {
            'nombre': {'required': True},
            'cantidad': {'required': True},
            'unidad': {'required': True},
            'precio_unitario': {'required': True}
        }

class recetaSerializer(serializers.ModelSerializer):
    insumo = insumoSerializer(many=True)

    class Meta:
        model = Receta
        fields = ['id', 'nombre', 'insumo', 'descripcion', 'porciones', 'categoria', 'fecha_creacion']
        read_only_fields = ['id', 'fecha_creacion']
        extra_kwargs = {
            'nombre': {'required': True},
            'insumo': {'required': True},
            'descripcion': {'required': True},
            'porciones': {'required': True},
            'categoria': {'required': True}
        }
    
    