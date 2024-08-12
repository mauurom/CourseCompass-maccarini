from rest_framework import serializers
from ..models.inscripcion import InscripcionMateria
#Selearizador para el modelo InscripcionMateria
class InscripcionMateriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = InscripcionMateria #Se especifica el modelo InscripcionMateria para el serealizador
        fields = ['id', 'estudiante', 'curso', 'fecha_inscripcion'] #Campos del modelo que se incluirán en la representación serializada
