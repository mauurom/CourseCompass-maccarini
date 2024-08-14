from django.test import TestCase
from accounts.forms.user_creation_form import UsuarioCreationForm, CustomUserChangeForm
from accounts.forms.user_authentication_form import UsuarioAuthenticationForm
from accounts.models.usuario import Usuario

# Pruebas para el formulario de creación de usuario
class UsuarioCreationFormTest(TestCase):
    # Prueba para verificar que el formulario es válido con datos correctos
    def test_usuario_creation_form_valid(self):
        form_data = {
            'dni': '12345678X',
            'correo': 'testuser@example.com',
            'nombre': 'Test',
            'apellido': 'User',
            'fecha_nacimiento': '2000-01-01',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'tipo_usuario': 'alumno'
        }
        form = UsuarioCreationForm(data=form_data)
        if not form.is_valid():
            print(form.errors)  # Imprimir errores si el formulario no es válido
        self.assertTrue(form.is_valid())  # Afirmar que el formulario es válido

    # Prueba para verificar que el formulario no es válido con datos incorrectos
    def test_usuario_creation_form_invalid(self):
        form_data = {
            'dni': '12345678X',
            'correo': 'invalidemail',
            'nombre': '',
            'apellido': '',
            'fecha_nacimiento': '2000-01-01',
            'password1': 'testpassword123',
            'password2': 'differentpassword',
            'tipo_usuario': 'alumno'
        }
        form = UsuarioCreationForm(data=form_data)
        self.assertFalse(form.is_valid())  # Afirmar que el formulario no es válido

# Pruebas para el formulario de modificación de usuario
class CustomUserChangeFormTest(TestCase):
    
    def setUp(self):  # Configuración inicial antes de las pruebas
        self.usuario = Usuario.objects.create_user(
            dni='12345678X',
            nombre='Test',
            apellido='User',
            correo='testuser@example.com',
            fecha_nacimiento='2000-01-01',
            password='testpassword123'
        )

    # Prueba para verificar que el formulario es válido con datos correctos
    def test_custom_user_change_form_valid(self):
        form_data = {
            'dni': '12345678X',
            'correo': 'newemail@example.com',
            'nombre': 'NewFirstName',
            'apellido': 'NewLastName',
            'fecha_nacimiento': '2000-01-01',
            'tipo_usuario': 'profesor'
        }
        form = CustomUserChangeForm(data=form_data, instance=self.usuario)
        if not form.is_valid():
            print(form.errors)  # Imprimir errores si el formulario no es válido
        self.assertTrue(form.is_valid())  # Afirmar que el formulario es válido

# Pruebas para el formulario de autenticación de usuario
class UsuarioAuthenticationFormTest(TestCase):
    def setUp(self):  # Configuración inicial antes de las pruebas
        self.usuario = Usuario.objects.create_user(
            dni='12345678X',
            nombre='Test',
            apellido='User',
            correo='testuser@example.com',
            fecha_nacimiento='2000-01-01',
            password='testpassword123'
        )

    # Prueba para verificar que el formulario es válido con credenciales correctas
    def test_usuario_authentication_form_valid(self):
        form_data = {
            'username': '12345678X',
            'password': 'testpassword123'
        }
        form = UsuarioAuthenticationForm(data=form_data)
        self.assertTrue(form.is_valid())  # Afirmar que el formulario es válido
        
    # Prueba para verificar que el formulario no es válido con credenciales incorrectas
    def test_usuario_authentication_form_invalid(self):
        form_data = {
            'username': '12345678X',
            'password': 'wrongpassword'
        }
        form = UsuarioAuthenticationForm(data=form_data)
        self.assertFalse(form.is_valid())  # Afirmar que el formulario no es válido
