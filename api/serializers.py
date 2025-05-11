from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Insumo, Receta, Venta, Merma, RecetaInsumo


# Serializador para el modelo de Usuario
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'email', 'password', 'first_name', 'last_name']
        extra_kwargs = {
            'password': {'write_only': True},
            'url': {'view_name': 'user-detail'}
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user


# Serializador para el modelo de Insumo
class InsumoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Insumo
        fields = ['url', 'id', 'nombre', 'cantidad', 'unidad', 'precio_unitario', 'fecha_creacion']
        read_only_fields = ['id', 'fecha_creacion']
        extra_kwargs = {
            'url': {'view_name': 'insumo-detail'},
            'nombre': {'required': True},
            'cantidad': {'required': True},
            'unidad': {'required': True},
            'precio_unitario': {'required': True}
        }

    def validate_cantidad(self, value):
        if value < 0:
            raise serializers.ValidationError("La cantidad no puede ser negativa")
        return value

    def validate_precio_unitario(self, value):
        if value < 0:
            raise serializers.ValidationError("El precio no puede ser negativo")
        return value

class RecetaInsumoSerializer(serializers.HyperlinkedModelSerializer):
    insumo_url = serializers.HyperlinkedRelatedField(
        view_name='insumo-detail',
        read_only=True,
        source='insumo'
    )
    insumo_nombre = serializers.CharField(source='insumo.nombre', read_only=True)
    insumo_unidad = serializers.CharField(source='insumo.unidad', read_only=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = RecetaInsumo
        fields = ['url', 'id', 'insumo', 'insumo_url', 'insumo_nombre', 'insumo_unidad', 
                 'cantidad', 'precio_unitario', 'subtotal']
        read_only_fields = ['precio_unitario', 'subtotal']
        extra_kwargs = {
            'url': {'view_name': 'recetainsumo-detail'},
            'insumo': {'view_name': 'insumo-detail'}
        }

    def validate_cantidad(self, value):
        if value <= 0:
            raise serializers.ValidationError("La cantidad debe ser mayor a 0")
        return value

class RecetaInsumoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecetaInsumo
        fields = ['insumo', 'cantidad']

class RecetaSerializer(serializers.HyperlinkedModelSerializer):
    insumos_detalle = RecetaInsumoSerializer(source='recetainsumo_set', many=True, read_only=True)
    insumos = RecetaInsumoCreateSerializer(many=True, write_only=True, required=False)
    costo_total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Receta
        fields = ['url', 'id', 'nombre', 'insumos', 'insumos_detalle', 'descripcion', 
                 'porciones', 'categoria', 'fecha_creacion', 'costo_total']
        read_only_fields = ['id', 'fecha_creacion', 'costo_total']
        extra_kwargs = {
            'url': {'view_name': 'receta-detail'}
        }

    def create(self, validated_data):
        insumos_data = validated_data.pop('insumos', [])
        receta = Receta.objects.create(**validated_data)
        
        for insumo_data in insumos_data:
            RecetaInsumo.objects.create(
                receta=receta,
                insumo_id=insumo_data['insumo'],
                cantidad=insumo_data['cantidad']
            )
        
        return receta

    def update(self, instance, validated_data):
        insumos_data = validated_data.pop('insumos', [])
        
        # Actualizar campos básicos
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Actualizar insumos si se proporcionaron
        if insumos_data:
            # Eliminar relaciones existentes
            instance.recetainsumo_set.all().delete()
            
            # Crear nuevas relaciones
            for insumo_data in insumos_data:
                RecetaInsumo.objects.create(
                    receta=instance,
                    insumo_id=insumo_data['insumo'],
                    cantidad=insumo_data['cantidad']
                )
        
        return instance

class VentaSerializer(serializers.HyperlinkedModelSerializer):
    recetas = RecetaSerializer(many=True, read_only=True)

    class Meta:
        model = Venta
        fields = ['url', 'id', 'recetas', 'fecha_venta', 'total', 'completada']
        extra_kwargs = {
            'url': {'view_name': 'venta-detail'},
            'recetas': {'view_name': 'receta-detail'}
        }

    def validate_total(self, value):
        if value < 0:
            raise serializers.ValidationError("El total no puede ser negativo")
        return value

class MermaSerializer(serializers.HyperlinkedModelSerializer):
    insumo_url = serializers.HyperlinkedRelatedField(
        view_name='insumo-detail',
        read_only=True,
        source='insumo'
    )
    insumo_nombre = serializers.CharField(source='insumo.nombre', read_only=True)

    class Meta:
        model = Merma
        fields = ['url', 'id', 'insumo', 'insumo_url', 'insumo_nombre', 'cantidad', 'fecha_merma']
        extra_kwargs = {
            'url': {'view_name': 'merma-detail'},
            'insumo': {'view_name': 'insumo-detail'}
        }

    def validate_cantidad(self, value):
        if value <= 0:
            raise serializers.ValidationError("La cantidad de merma debe ser mayor a 0")
        return value
    
    