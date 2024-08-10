from django.db import models
from .curso import Curso
from django.core.exceptions import ValidationError
from django.utils import timezone

class Tarea(models.Model):
    
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='tareas')#Relación con el modelo Curso
    titulo = models.CharField(max_length=100)                       #Título de la tarea
    descripcion = models.TextField()                                #Descripción de la tarea
    fecha_entrega = models.DateTimeField()                          #Fecha y hora en que debe entregarse la tarea

    def __str__(self):
        return self.titulo

    def clean(self):
        
        if self.fecha_entrega < timezone.now():   #Verifica que la fecha de entrega no sea en el pasado
            raise ValidationError('La fecha de entrega no puede ser en el pasado.')

    class Meta:
        
        ordering = ['fecha_entrega'] #Ordena las tareas por fecha de entrega
