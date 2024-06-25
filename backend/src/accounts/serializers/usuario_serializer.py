from rest_framework import serializers
from ..models.usuario import Usuario

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['dni', 'nombre', 'apellido', 'correo', 'fecha_nacimiento', 'tipo_usuario', 'is_active', 'is_admin', 'is_staff', 'is_superuser']
