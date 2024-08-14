from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from accounts.models.usuario import Usuario

# Pruebas para las vistas de la API de autenticación
class LoginAPIViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()  # Configuración inicial del cliente de prueba
        self.usuario = Usuario.objects.create_user(
            dni='12345678X',
            nombre='Test',
            apellido='User',
            correo='testuser@example.com',
            fecha_nacimiento='2000-01-01',
            password='testpassword123'
        )
        self.login_url = reverse('login')

    # Prueba para verificar el inicio de sesión con credenciales válidas
    def test_login_valid_credentials(self):
        response = self.client.post(self.login_url, {
            'username': '12345678X',
            'password': 'testpassword123'
        })
        self.assertEqual(response.status_code, 200)  # Afirmar que la respuesta sea 200
        self.assertIn('token', response.data)  # Afirmar que el token esté en la respuesta

    # Prueba para verificar el inicio de sesión con credenciales inválidas
    def test_login_invalid_credentials(self):
        response = self.client.post(self.login_url, {
            'username': '12345678X',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 400)  # Afirmar que la respuesta sea 400
        self.assertNotIn('token', response.data)  # Afirmar que el token no esté en la respuesta
