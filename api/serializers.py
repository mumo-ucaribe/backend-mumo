from rest_framework import serializers
from .models import receta, insumo, venta, merma, User

class UserSerializer(serializers.ModelSerializer):
    