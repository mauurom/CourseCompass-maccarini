from django.contrib import admin
from .models import Curso, InscripcionMateria, Tarea, Entrega

admin.site.register(Curso)                   #Registra el modelo Curso en el sitio de Administracion
admin.site.register(InscripcionMateria)      #Registra el modelo de InscripcionMateria en el sitio de Administracion 
admin.site.register(Tarea)                   #Registra el modelo Tarea en el sitio de Administracion
admin.site.register(Entrega)                 #Registra el modelo Entrega en el sistio Administracion