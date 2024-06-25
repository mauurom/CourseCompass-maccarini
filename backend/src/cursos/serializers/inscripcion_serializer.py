from rest_framework import serializers
from ..models.inscripcion import InscripcionMateria

class InscripcionMateriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = InscripcionMateria
        fields = ['id', 'estudiante', 'curso', 'fecha_inscripcion']
