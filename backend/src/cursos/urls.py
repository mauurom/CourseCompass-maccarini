from django.urls import path
from .views import crear_tarea, entregar_tarea, tarea_detalle, curso_detalle, lista_cursos, crear_curso

urlpatterns = [
    path('tarea/crear/<int:curso_id>/', crear_tarea, name='crear_tarea'),
    path('tarea/entregar/<int:tarea_id>/', entregar_tarea, name='entregar_tarea'),
    path('tarea/detalle/<int:tarea_id>/', tarea_detalle, name='tarea_detalle'),
    path('crear_curso/', crear_curso, name='crear_curso'),
    path('curso_detalle/<int:curso_id>/', curso_detalle, name='curso_detalle'),
    path('lista_cursos/', lista_cursos, name='lista_cursos'),
]