from django.contrib import admin
from .models import Curso, InscripcionMateria, Tarea, Entrega

admin.site.register(Curso)
admin.site.register(InscripcionMateria)
admin.site.register(Tarea)
admin.site.register(Entrega)