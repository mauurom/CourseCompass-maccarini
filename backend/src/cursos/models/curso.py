from django.db import models
from accounts.models import Profesor
from django.core.exceptions import ValidationError
from django.utils import timezone

class Curso(models.Model):
   
    nombre = models.CharField(max_length=100)                   #Nombre del curso.
    descripcion = models.TextField()                            #Descripción del curso.
    año = models.PositiveIntegerField()                         #Año en que se ofrece el curso.
    horario = models.CharField(max_length=50)                   #Horario del curso.
    contraseña_matriculacion = models.CharField(max_length=50)  #Contraseña para la matriculación en el curso.
    profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE, related_name='cursos')# Relación con el modelo Profesor.

    def __str__(self):
        return self.nombre

    def clean(self):
        if self.año < timezone.now().year:                      # Valida que el año del curso no sea en el pasado.
            raise ValidationError('El año del curso no puede ser en el pasado.')

    class Meta:
        ordering = ['año', 'nombre']                           # Ordena los cursos por año y nombre.
