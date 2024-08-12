from rest_framework import serializers
from ..models.usuario import Usuario

#Serealizador para el modelo usuario
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario #Se especifica el modelo Usuario para el serealizador 
        #Campos del modelo que se incluiran en la representacion del serealizada
        fields = ['dni', 'nombre', 'apellido', 'correo', 'fecha_nacimiento', 'tipo_usuario', 'is_active', 'is_admin', 'is_staff', 'is_superuser']
