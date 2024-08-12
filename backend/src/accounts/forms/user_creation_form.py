from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from ..models.usuario import Usuario

# Formulario para la creación de un nuevo usuario
class UsuarioCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = Usuario               #Se especifica el modelo Usuario para el formulario
        fields = ('dni', 'correo', 'nombre', 'apellido', 'fecha_nacimiento', 'tipo_usuario') #Campos del formulario que se mostrarán y serán rellenados

# Formulario personalizado para la modificación de un usuario existente
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = Usuario              #Se especifica el modelo Usuario para el formulario
        fields = ('dni', 'correo', 'nombre', 'apellido', 'fecha_nacimiento', 'tipo_usuario') #Campos del formulario que se pueden modificar
