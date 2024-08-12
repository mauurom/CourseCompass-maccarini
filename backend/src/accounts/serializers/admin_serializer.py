from rest_framework import serializers
from ..models.admin import Admin

# Serializador para el modelo Admin
class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin  #Se especifica el modelo Admin para el serializador
        fields = ['usuario', 'nombre_usuario']  #Campos del modelo que se incluirán en la representación serializada
