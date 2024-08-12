from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from cursos.models.curso import Curso
from cursos.models.tarea import Tarea
from cursos.models.entrega import Entrega
from accounts.models.profesor import Profesor
from accounts.models.alumno import Alumno
from django.utils.timezone import make_aware
from datetime import datetime

class EntregaTestCase(TestCase):
    def setUp(self):
        #Configura los datos iniciales para las pruebas
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
        self.tarea = Tarea.objects.create(
            curso=self.curso,
            titulo='Tarea de Prueba',
            descripcion='Descripción de la tarea',
            fecha_entrega=make_aware(datetime(2024, 6, 30, 12, 0, 0))
        )
        self.entrega = Entrega.objects.create(
            tarea=self.tarea,
            estudiante=self.alumno,
            archivo='cursos/tests/fixtures/test_file.txt',
            comentario='Comentario de prueba',
            fecha_entrega=make_aware(datetime(2024, 6, 25, 12, 0, 0))
        )

    #Prueba la funcionalidad de entrega de tareas
    def test_entregar_tarea(self):
        #Inicia sesión como alumno
        self.client.login(dni='87654321', password='password')
        #Envía una solicitud POST para entregar la tarea
        with open('cursos/tests/fixtures/test_file.txt', 'rb') as f:
            response = self.client.post(reverse('entregar_tarea', kwargs={'tarea_id': self.tarea.id}), {
                'archivo': f,
                'comentario': 'Comentario de prueba'
            })
        #Verifica que la respuesta sea exitosa
        self.assertEqual(response.status_code, 200)
        #Verifica que la entrega se haya guardado en la base de datos
        self.assertTrue(Entrega.objects.filter(tarea=self.tarea, estudiante=self.alumno).exists())
