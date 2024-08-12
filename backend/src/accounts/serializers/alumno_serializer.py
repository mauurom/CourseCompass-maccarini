from rest_framework import serializers
from ..models.alumno import Alumno

# Serializador para el modelo Alumno
class AlumnoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alumno#Se especifica el modelo Alumno para el serializador
        fields = ['usuario', 'legajo_alumno']#Campos del modelo que se incluirán en la representación serializada
