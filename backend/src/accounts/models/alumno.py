from django.db import models
from django.core.validators import MaxValueValidator
from .usuario import Usuario

class Alumno(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True)
    legajo_alumno = models.IntegerField(validators=[MaxValueValidator(99999)], unique=True)

    def __str__(self):
        return f"{self.usuario.nombre} {self.usuario.apellido} - Alumno"
