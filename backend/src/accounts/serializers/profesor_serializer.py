from rest_framework import serializers
from ..models.profesor import Profesor

#Serealizador para el modelo Profesor
class ProfesorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profesor #Se especifica el modelo Profesor para el serializador
        fields = ['usuario', 'legajo_profesor'] #Campos del modelo que se incluiran en la representacion serealizada
