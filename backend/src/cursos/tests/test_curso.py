from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from cursos.models.curso import Curso
from cursos.models.tarea import Tarea
from cursos.models.entrega import Entrega
from accounts.models.profesor import Profesor
from accounts.models.alumno import Alumno

class CursoTestCase(TestCase):
    def setUp(self):
        # Configura los datos iniciales para las pruebas
        self.user_profesor = get_user_model().objects.create_user(
            dni='12345678',
            nombre='ProfesorNombre',
            apellido='ProfesorApellido',
            correo='profesor@example.com',
            fecha_nacimiento='1980-01-01',
            password='password'
        )
        self.profesor = Profesor.objects.create(
            usuario=self.user_profesor,
            legajo_profesor=124
        )
        self.curso = Curso.objects.create(
            nombre='Curso de Prueba',
            descripcion='Descripción de prueba',
            año=2024,
            horario='Lunes 10:00 - 12:00',
            contraseña_matriculacion='testpass',
            profesor=self.profesor
        )
        self.user_alumno = get_user_model().objects.create_user(
            dni='87654321',
            nombre='AlumnoNombre',
            apellido='AlumnoApellido',
            correo='alumno@example.com',
            fecha_nacimiento='2000-01-01',
            password='password'
        )
        self.alumno = Alumno.objects.create(
            usuario=self.user_alumno,
            legajo_alumno=123
        )

    # Prueba la creación de un nuevo curso
    def test_crear_curso(self):
        self.client.login(dni='12345678', password='password')
        response = self.client.post(reverse('crear_curso'), {
            'nombre': 'Nuevo Curso',
            'descripcion': 'Descripción del nuevo curso',
            'año': 2025,
            'horario': 'Martes 14:00 - 16:00',
            'contraseña_matriculacion': 'nuevapass',
        })
        self.assertEqual(response.status_code, 201)              #Verifica que la creación fue exitosa
        self.assertTrue(Curso.objects.filter(nombre='Nuevo Curso').exists())  #Verifica que el nuevo curso existe

    # Prueba la lista de cursos
    def test_lista_cursos(self):
        self.client.login(dni='12345678', password='password')
        response = self.client.get(reverse('lista_cursos'))
        self.assertEqual(response.status_code, 200)              #Verifica que la solicitud fue exitosa
        self.assertContains(response, self.curso.nombre)         #Verifica que el curso de prueba está en la lista

    # Prueba los detalles de un curso específico
    def test_curso_detalle(self):
        self.client.login(dni='12345678', password='password')
        response = self.client.get(reverse('curso_detalle', kwargs={'curso_id': self.curso.id}))
        self.assertEqual(response.status_code, 200)              #Verifica que la solicitud fue exitosa
        self.assertContains(response, self.curso.nombre)         # erifica que el nombre del curso está en la respuesta
