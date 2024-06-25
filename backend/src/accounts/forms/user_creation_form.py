from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from ..models.usuario import Usuario

class UsuarioCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = Usuario
        fields = ('dni', 'correo', 'nombre', 'apellido', 'fecha_nacimiento', 'tipo_usuario')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = Usuario
        fields = ('dni', 'correo', 'nombre', 'apellido', 'fecha_nacimiento', 'tipo_usuario')
