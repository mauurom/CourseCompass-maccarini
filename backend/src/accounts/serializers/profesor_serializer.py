from rest_framework import serializers
from ..models.profesor import Profesor

class ProfesorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profesor
        fields = ['usuario', 'legajo_profesor']
