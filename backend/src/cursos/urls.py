from django.urls import path
from .views import crear_tarea, entregar_tarea, tarea_detalle, curso_detalle, lista_cursos, crear_curso

#Definicion de rutas para la app de cursos
urlpatterns = [
    path('tarea/crear/<int:curso_id>/', crear_tarea, name='crear_tarea'),               #Ruta para crear una tarea en un curso especifico
    path('tarea/entregar/<int:tarea_id>/', entregar_tarea, name='entregar_tarea'),      #Ruta para entregar una tarea especifica
    path('tarea/detalle/<int:tarea_id>/', tarea_detalle, name='tarea_detalle'),         #Ruta para ver los detalles de una tarea especifica
    path('crear_curso/', crear_curso, name='crear_curso'),                              #Ruta para crear un nuevo curso
    path('curso_detalle/<int:curso_id>/', curso_detalle, name='curso_detalle'),         #Ruta para ver los detalles de un curso especifico
    path('lista_cursos/', lista_cursos, name='lista_cursos'),                           #ruta para listar todos los cursos disponibles
]