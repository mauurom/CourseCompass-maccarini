from rest_framework import serializers
from ..models.tarea import Tarea

class TareaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarea
        fields = ['id', 'curso', 'titulo', 'descripcion', 'fecha_entrega']
