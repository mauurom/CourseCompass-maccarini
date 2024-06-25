from rest_framework import serializers
from ..models.alumno import Alumno

class AlumnoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alumno
        fields = ['usuario', 'legajo_alumno']
