from django.db import models
from django.core.validators import MaxValueValidator
from .usuario import Usuario

class Profesor(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True)
    legajo_profesor = models.IntegerField(validators=[MaxValueValidator(99999)], unique=True) #El numero de legajo del profesor debe ser unico y no mayor a 99999

    def __str__(self):
        return f"{self.usuario.nombre} {self.usuario.apellido} - Profesor"
