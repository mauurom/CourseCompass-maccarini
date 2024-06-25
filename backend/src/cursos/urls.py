from django.urls import path
from .views import curso_view, tarea_view

urlpatterns = [
    path('', curso_view.lista_cursos, name='lista_cursos'),
    path('curso/<int:curso_id>/', curso_view.curso_detalle, name='curso_detalle'),
    path('crear_curso/', curso_view.crear_curso, name='crear_curso'),
    path('curso/<int:curso_id>/crear_tarea/', tarea_view.crear_tarea, name='crear_tarea'),
    path('tarea/<int:tarea_id>/entregar/', tarea_view.entregar_tarea, name='entregar_tarea'),
    path('tarea/<int:tarea_id>/', tarea_view.tarea_detalle, name='tarea_detalle'),
]
