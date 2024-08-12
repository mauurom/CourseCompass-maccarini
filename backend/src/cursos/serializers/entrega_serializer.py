from rest_framework import serializers
from ..models.tarea import Tarea

#Selearizador para el modelo Tarea
class TareaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarea #Se especifica el modelo Tarea para el serealizador
        fields = ['id', 'curso', 'titulo', 'descripcion', 'fecha_entrega'] #Campos del modelo que se incluirán en la representación serializada
