from django.db import models
from .curso import Curso
from django.core.exceptions import ValidationError
from django.utils import timezone

class Tarea(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='tareas')
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_entrega = models.DateTimeField()

    def __str__(self):
        return self.titulo

    def clean(self):
        if self.fecha_entrega < timezone.now():
            raise ValidationError('La fecha de entrega no puede ser en el pasado.')

    class Meta:
        ordering = ['fecha_entrega']
