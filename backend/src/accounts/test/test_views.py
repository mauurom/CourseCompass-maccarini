from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from accounts.models.usuario import Usuario

# Pruebas para las vistas de autenticación.
class AuthViewsTest(TestCase):
    def setUp(self):
        # Configura el cliente API y crea un usuario de prueba.
        self.client = APIClient()
        self.usuario_data = {
            'dni': '12345678X',
            'nombre': 'Test',
            'apellido': 'User',
            'correo': 'testuser@example.com',
            'fecha_nacimiento': '2000-01-01',
            'password': 'testpassword123',
            'tipo_usuario': 'alumno'
        }
        self.usuario = Usuario.objects.create_user(**self.usuario_data)
        self.usuario.set_password(self.usuario_data['password'])
        self.usuario.save()

    # Prueba la vista de inicio de sesión con credenciales válidas.
    def test_login_view(self):
        url = reverse('login')
        response = self.client.post(url, {
            'dni': self.usuario_data['dni'],
            'password': self.usuario_data['password']
        })
        self.assertEqual(response.status_code, 200)

    # Prueba la vista de inicio de sesión con credenciales inválidas.
    def test_login_view_invalid_credentials(self):
        url = reverse('login')
        response = self.client.post(url, {
            'dni': self.usuario_data['dni'],
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 401)

    # Prueba la vista de registro con datos válidos.
    def test_register_view(self):
        url = reverse('register')
        response = self.client.post(url, {
            'dni': '87654321X',
            'nombre': 'New',
            'apellido': 'User',
            'correo': 'newuser@example.com',
            'fecha_nacimiento': '1990-01-01',
            'password': 'newpassword123',
            'tipo_usuario': 'profesor'
        })
        self.assertEqual(response.status_code, 201)

    # Prueba la vista de registro con datos inválidos.
    def test_register_view_invalid_data(self):
        url = reverse('register')
        response = self.client.post(url, {
            'dni': '87654321X',
            'nombre': '',
            'apellido': 'User',
            'correo': 'newuser@example.com',
            'fecha_nacimiento': '1990-01-01',
            'password': 'newpassword123',
            'tipo_usuario': 'profesor'
        })
        self.assertEqual(response.status_code, 400)
