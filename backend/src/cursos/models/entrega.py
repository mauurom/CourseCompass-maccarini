from django.db import models
from .tarea import Tarea
from accounts.models import Alumno
from django.core.exceptions import ValidationError

class Entrega(models.Model):
    tarea = models.ForeignKey(Tarea, on_delete=models.CASCADE, related_name='entregas')
    estudiante = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name='entregas')
    archivo = models.FileField(upload_to='entregas/')
    comentario = models.TextField(blank=True, null=True)
    fecha_entrega = models.DateTimeField(auto_now_add=True)
    calificacion = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f'{self.tarea.titulo} - {self.estudiante.usuario.username}'

    def clean(self):
        if self.calificacion is not None and (self.calificacion < 0 or self.calificacion > 10):
            raise ValidationError('La calificación debe estar entre 0 y 10.')

    class Meta:
        ordering = ['fecha_entrega']
