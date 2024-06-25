from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, dni, nombre, apellido, correo, password=None, **extra_fields):
        if not correo:
            raise ValueError('El usuario debe tener un correo electrónico')
        
        user = self.model(
            dni=dni,
            nombre=nombre,
            apellido=apellido,
            correo=self.normalize_email(correo),
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, dni, nombre, apellido, correo, password, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_admin') is not True:
            raise ValueError('Superuser must have is_admin=True.')

        return self.create_user(dni, nombre, apellido, correo, password, **extra_fields)

class Usuario(AbstractBaseUser, PermissionsMixin):
    dni = models.CharField(max_length=10, unique=True)
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    correo = models.EmailField(unique=True)
    fecha_nacimiento = models.DateField()
    tipo_usuario = models.CharField(max_length=10, choices=[('alumno', 'Alumno'), ('profesor', 'Profesor')], default='alumno')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'dni'
    REQUIRED_FIELDS = ['nombre', 'apellido', 'correo', 'fecha_nacimiento']

    def __str__(self):
        return f'{self.nombre} {self.apellido}'

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin
