from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from cursos.models.curso import Curso
from cursos.models.tarea import Tarea
from cursos.models.entrega import Entrega
from accounts.models.profesor import Profesor
from accounts.models.alumno import Alumno
from django.utils.timezone import make_aware
import datetime

class TareaTestCase(TestCase):
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
            horario='Lunes 10:00 - 20:00',
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
            fecha_entrega=make_aware(datetime.datetime(2024, 7, 8, 17, 0, 0))
        )

    # Prueba la creación de una nueva tarea
    def test_crear_tarea(self):
        self.client.login(dni='12345678', password='password')          #Inicia sesión como profesor
        response = self.client.post(reverse('crear_tarea', kwargs={'curso_id': self.curso.id}), {   #Envía una solicitud POST para crear una nueva tarea
            'titulo': 'Nueva Tarea',
            'descripcion': 'Descripción de la nueva tarea',
            'fecha_entrega': '2024-08-07 20:00:00',
        })
        # Imprime los errores de la respuesta en caso de que el código de estado sea 400 (Bad Request)
        if response.status_code == 400:
            print(response.json())                                      #Imprimir el contenido de la respuesta en caso de error
        self.assertEqual(response.status_code, 201)                     #Verifica que la respuesta sea exitosa
        self.assertTrue(Tarea.objects.filter(titulo='Nueva Tarea').exists()) #Verifica que la nueva tarea se haya creado en la base de datos

    # Prueba la entrega de una tarea
    def test_entregar_tarea(self):
        
        self.client.login(dni='87654321', password='password')          #Inicia sesión como alumno
        with open('cursos/tests/fixtures/test_file.txt', 'w') as f:     #Crea un archivo de prueba para la entrega
            f.write('contenido de prueba')
        with open('cursos/tests/fixtures/test_file.txt', 'rb') as f:    #Envía una solicitud POST para entregar la tarea
            response = self.client.post(reverse('entregar_tarea', kwargs={'tarea_id': self.tarea.id}), {
                'archivo': f,
                'comentario': 'Comentario de prueba'
            })
        self.assertEqual(response.status_code, 200)                     #Verifica que la respuesta sea exitosa
        self.assertTrue(Entrega.objects.filter(tarea=self.tarea, estudiante=self.alumno).exists())#Verifica que la entrega se haya guardado en la base de datos

    #Prueba la visualización de los detalles de una tarea
    def test_tarea_detalle(self):
        self.client.login(dni='12345678', password='password')          #Inicia sesión como profesor
        response = self.client.get(reverse('tarea_detalle', kwargs={'tarea_id': self.tarea.id}))#Envía una solicitud GET para obtener los detalles de la tarea
        self.assertEqual(response.status_code, 200)                     #Verifica que la respuesta sea exitosa
        self.assertContains(response, self.tarea.titulo)                #Verifica que el título de la tarea esté presente en la respuesta
