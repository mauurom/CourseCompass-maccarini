from django.db import models
from accounts.models import Alumno
from .curso import Curso
from django.core.exceptions import ValidationError
from django.utils import timezone

class InscripcionMateria(models.Model):
    estudiante = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    fecha_inscripcion = models.DateField()

    class Meta:
        db_table = 'inscripciones_estudiantes'
        unique_together = ('estudiante', 'curso')

    def __str__(self):
        return f'Inscripción de {self.estudiante} en {self.curso}'

    def clean(self):
        if self.fecha_inscripcion > timezone.now().date():
            raise ValidationError('La fecha de inscripción no puede ser en el futuro.')
