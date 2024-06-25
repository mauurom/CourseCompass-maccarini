from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from ..models.curso import Curso
from accounts.models.profesor import Profesor

class CursoTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(dni='12345678', password='password')
        self.profesor = Profesor.objects.create(usuario=self.user)
        self.curso = Curso.objects.create(
            nombre='Curso de Prueba',
            descripcion='Descripción de prueba',
            año=2024,
            horario='Lunes 10:00 - 12:00',
            contraseña_matriculacion='testpass',
            profesor=self.profesor
        )

    def test_curso_detalle(self):
        self.client.login(dni='12345678', password='password')
        response = self.client.get(reverse('curso_detalle', kwargs={'curso_id': self.curso.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.curso.nombre)

    def test_lista_cursos(self):
        self.client.login(dni='12345678', password='password')
        response = self.client.get(reverse('lista_cursos'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.curso.nombre)

    def test_crear_curso(self):
        self.client.login(dni='12345678', password='password')
        response = self.client.post(reverse('crear_curso'), {
            'nombre': 'Nuevo Curso',
            'descripcion': 'Descripción del nuevo curso',
            'año': 2024,
            'horario': 'Martes 14:00 - 16:00',
            'contraseña_matriculacion': 'nuevopass',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Curso.objects.filter(nombre='Nuevo Curso').exists())
