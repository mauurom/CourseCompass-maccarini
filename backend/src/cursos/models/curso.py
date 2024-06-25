from django.db import models
from accounts.models import Profesor
from django.core.exceptions import ValidationError
from django.utils import timezone

class Curso(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    año = models.PositiveIntegerField()
    horario = models.CharField(max_length=50)
    contraseña_matriculacion = models.CharField(max_length=50)
    profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE, related_name='cursos')

    def __str__(self):
        return self.nombre

    def clean(self):
        if self.año < timezone.now().year:
            raise ValidationError('El año del curso no puede ser en el pasado.')

    class Meta:
        ordering = ['año', 'nombre']
