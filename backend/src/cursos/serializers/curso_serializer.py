from rest_framework import serializers
from ..models.curso import Curso

# Serializador para el modelo Curso
class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso           #Se especifica el modelo Curso para el serializador
        fields = ['id', 'nombre', 'descripcion', 'año', 'horario', 'contraseña_matriculacion', 'profesor'] #Campos del modelo que se incluirán en la representación serializada
