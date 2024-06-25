from django.test import TestCase
from accounts.models.usuario import Usuario
from accounts.models.alumno import Alumno
from accounts.models.profesor import Profesor
from accounts.models.admin import Admin

class UsuarioModelTest(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create_user(
            dni='12345678X',
            nombre='Test',
            apellido='User',
            correo='testuser@example.com',
            fecha_nacimiento='2000-01-01',
            password='testpassword123'
        )

    def test_usuario_creation(self):
        self.assertEqual(self.usuario.dni, '12345678X')
        self.assertEqual(self.usuario.nombre, 'Test')
        self.assertEqual(self.usuario.apellido, 'User')
        self.assertEqual(self.usuario.correo, 'testuser@example.com')
        self.assertTrue(self.usuario.check_password('testpassword123'))
        self.assertTrue(self.usuario.is_active)
        self.assertFalse(self.usuario.is_admin)
        self.assertFalse(self.usuario.is_staff)
        self.assertFalse(self.usuario.is_superuser)

    def test_usuario_str(self):
        self.assertEqual(str(self.usuario), 'Test User')

class AlumnoModelTest(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create_user(
            dni='12345678X',
            nombre='Test',
            apellido='User',
            correo='testuser@example.com',
            fecha_nacimiento='2000-01-01',
            password='testpassword123'
        )
        self.alumno = Alumno.objects.create(
            usuario=self.usuario,
            legajo_alumno=12345
        )

    def test_alumno_creation(self):
        self.assertEqual(self.alumno.usuario, self.usuario)
        self.assertEqual(self.alumno.legajo_alumno, 12345)

    def test_alumno_str(self):
        self.assertEqual(str(self.alumno), 'Test User - Alumno')

class ProfesorModelTest(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create_user(
            dni='12345678X',
            nombre='Test',
            apellido='User',
            correo='testuser@example.com',
            fecha_nacimiento='2000-01-01',
            password='testpassword123'
        )
        self.profesor = Profesor.objects.create(
            usuario=self.usuario,
            legajo_profesor=54321
        )

    def test_profesor_creation(self):
        self.assertEqual(self.profesor.usuario, self.usuario)
        self.assertEqual(self.profesor.legajo_profesor, 54321)

    def test_profesor_str(self):
        self.assertEqual(str(self.profesor), 'Test User - Profesor')

class AdminModelTest(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create_user(
            dni='12345678X',
            nombre='Test',
            apellido='User',
            correo='testuser@example.com',
            fecha_nacimiento='2000-01-01',
            password='testpassword123',
            is_admin=True
        )
        self.admin = Admin.objects.create(
            usuario=self.usuario,
            nombre_usuario='adminuser'
        )

    def test_admin_creation(self):
        self.assertEqual(self.admin.usuario, self.usuario)
        self.assertEqual(self.admin.nombre_usuario, 'adminuser')

    def test_admin_str(self):
        self.assertEqual(str(self.admin), 'adminuser - Admin')
