from django.test import TestCase
from accounts.models.usuario import Usuario
from accounts.models.alumno import Alumno
from accounts.models.profesor import Profesor
from accounts.models.admin import Admin

# Pruebas para el modelo Usuario
class UsuarioModelTest(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create_user(         #Configuración inicial antes de las pruebas, creando un usuario
            dni='12345678X',
            nombre='Test',
            apellido='User',
            correo='testuser@example.com',
            fecha_nacimiento='2000-01-01',
            password='testpassword123'
        )

    # Prueba para verificar la creación del usuario y sus atributos
    def test_usuario_creation(self):
        self.assertEqual(self.usuario.dni, '12345678X')
        self.assertEqual(self.usuario.nombre, 'Test')
        self.assertEqual(self.usuario.apellido, 'User')
        self.assertEqual(self.usuario.correo, 'testuser@example.com')
        self.assertTrue(self.usuario.check_password('testpassword123'))  # Verifica la contraseña
        self.assertTrue(self.usuario.is_active)             #Verifica que el usuario esté activo
        self.assertFalse(self.usuario.is_admin)             #Verifica que el usuario no es admin
        self.assertFalse(self.usuario.is_staff)             #Verifica que el usuario no es staff
        self.assertFalse(self.usuario.is_superuser)         #Verifica que el usuario no es superuser

    # Prueba para verificar la representación en cadena del usuario
    def test_usuario_str(self):
        self.assertEqual(str(self.usuario), 'Test User')

# Pruebas para el modelo Alumno
class AlumnoModelTest(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create_user(         #Configuración inicial antes de las pruebas, creando un usuario y un alumno
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

    # Prueba para verificar la creación del alumno y sus atributos
    def test_alumno_creation(self):
        self.assertEqual(self.alumno.usuario, self.usuario)
        self.assertEqual(self.alumno.legajo_alumno, 12345)

    # Prueba para verificar la representación en cadena del alumno
    def test_alumno_str(self):
        self.assertEqual(str(self.alumno), 'Test User - Alumno')

# Pruebas para el modelo Profesor
class ProfesorModelTest(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create_user(           #Configuración inicial antes de las pruebas, creando un usuario y un profesor
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

    # Prueba para verificar la creación del profesor y sus atributos
    def test_profesor_creation(self):
        self.assertEqual(self.profesor.usuario, self.usuario)
        self.assertEqual(self.profesor.legajo_profesor, 54321)

    # Prueba para verificar la representación en cadena del profesor
    def test_profesor_str(self):
        self.assertEqual(str(self.profesor), 'Test User - Profesor')

# Pruebas para el modelo Admin
class AdminModelTest(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create_user(             #Configuración inicial antes de las pruebas, creando un usuario con rol de admin y un admin
            dni='12345678X',
            nombre='Test',
            apellido='User',
            correo='testuser@example.com',
            fecha_nacimiento='2000-01-01',
            password='testpassword123',
            is_admin=True                                       #Define al usuario como admin
        )
        self.admin = Admin.objects.create(
            usuario=self.usuario,
            nombre_usuario='adminuser'
        )

    # Prueba para verificar la creación del admin y sus atributos
    def test_admin_creation(self):
        self.assertEqual(self.admin.usuario, self.usuario)
        self.assertEqual(self.admin.nombre_usuario, 'adminuser')

    # Prueba para verificar la representación en cadena del admin
    def test_admin_str(self):
        self.assertEqual(str(self.admin), 'adminuser - Admin')
