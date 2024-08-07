from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from ..models import Curso, Profesor, Tarea, Entrega
from rest_framework.test import APIClient

class TareaDetalleTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_profesor = get_user_model().objects.create_user(
            dni='12345678',
            nombre='ProfesorNombre',
            apellido='ProfesorApellido',
            correo='profesor@example.com',
            fecha_nacimiento='1980-01-01',
            password='password'
        )
        self.profesor = Profesor.objects.create(usuario=self.user_profesor, legajo_profesor=123)
        self.curso = Curso.objects.create(
            nombre='Curso 1',
            descripcion='Descripción del curso 1',
            año=2024,
            horario='Lunes 10am',
            contraseña_matriculacion='1234',
            profesor=self.profesor
        )
        self.client.force_authenticate(user=self.user_profesor)

        self.tarea = Tarea.objects.create(
            curso=self.curso,
            titulo='Tarea 1',
            descripcion='Descripción de la tarea 1',
            fecha_entrega='2024-12-01'
        )

    def test_tarea_detalle(self):
        response = self.client.get(reverse('tarea_detalle', kwargs={'tarea_id': self.tarea.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['tarea_id'], self.tarea.id)
