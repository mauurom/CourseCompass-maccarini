from django.db import models
from accounts.models import Alumno
from .curso import Curso
from django.core.exceptions import ValidationError
from django.utils import timezone

class InscripcionMateria(models.Model):
    
    estudiante = models.ForeignKey(Alumno, on_delete=models.CASCADE) #Relación con el modelo Alumno
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)       #Relación con el modelo Curso
    fecha_inscripcion = models.DateField()                           #Fecha de inscripción del estudiante en el curso

    class Meta:
        db_table = 'inscripciones_estudiantes'    #Define el nombre de la tabla en la base de datos
        unique_together = ('estudiante', 'curso') #Verifica que la combinación de estudiante y curso sea única

    def __str__(self):
        return f'Inscripción de {self.estudiante} en {self.curso}'

    def clean(self):
        if self.fecha_inscripcion > timezone.now().date(): #Valida que la fecha de inscripción no sea en el futuro
            raise ValidationError('La fecha de inscripción no puede ser en el futuro.')
