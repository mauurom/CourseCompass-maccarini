from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, dni, nombre, apellido, correo, password=None, **extra_fields):
        #Verifica que el correo no esté vacío
        if not correo:
            raise ValueError('El usuario debe tener un correo electrónico')
        
        #Crea una nueva instancia de usuario
        user = self.model(
            dni=dni,
            nombre=nombre,
            apellido=apellido,
            correo=self.normalize_email(correo),
            **extra_fields,
        )
       
        user.set_password(password)                     #Establece la contraseña del usuario
        user.save(using=self._db)
        return user

    def create_superuser(self, dni, nombre, apellido, correo, password, **extra_fields):
        extra_fields.setdefault('is_admin', True)       #Configura los permisos del superusuario
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_admin') is not True:    #Verifica que el superusuario tenga el permiso de admin
            raise ValueError('Superuser must have is_admin=True.')

        return self.create_user(dni, nombre, apellido, correo, password, **extra_fields)

class Usuario(AbstractBaseUser, PermissionsMixin):
    
    dni = models.CharField(max_length=10, unique=True)  #Documento de identidad del usuario
    nombre = models.CharField(max_length=30)            #Nombre del usuario
    apellido = models.CharField(max_length=30)          #Apellido del usuario
    correo = models.EmailField(unique=True)             #Correo electrónico del usuario
    fecha_nacimiento = models.DateField()               #Fecha de nacimiento del usuario
    #Tipo de usuario (Alumno o Profesor)
    tipo_usuario = models.CharField(max_length=10, choices=[('alumno', 'Alumno'), ('profesor', 'Profesor')], default='alumno')
    is_active = models.BooleanField(default=True)       #Estado activo del usuario
    is_admin = models.BooleanField(default=False)       #Permiso de admin
    is_staff = models.BooleanField(default=False)       #Permiso de staff
    is_superuser = models.BooleanField(default=False)   #Permiso de superusuario

    objects = UserManager()

    USERNAME_FIELD = 'dni'
    REQUIRED_FIELDS = ['nombre', 'apellido', 'correo', 'fecha_nacimiento']

    def __str__(self):
        return f'{self.nombre} {self.apellido}'

    def has_perm(self, perm, obj=None): 
        return self.is_admin               #Verifica si el usuario tiene un permiso específico

    def has_module_perms(self, app_label):
        return self.is_admin               #Verifica si el usuario tiene permisos de módulo
