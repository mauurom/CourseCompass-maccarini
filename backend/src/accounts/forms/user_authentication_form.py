from django.contrib.auth.forms import AuthenticationForm

from ..models import Usuario

# Definir el formulario de autenticación de usuario
class UsuarioAuthenticationForm(AuthenticationForm):
    class Meta:
        model = Usuario
        fields = ('dni', 'password')
