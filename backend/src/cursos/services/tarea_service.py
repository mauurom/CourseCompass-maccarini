from django.shortcuts import get_object_or_404
from django.utils import timezone
from ..models.tarea import Tarea
from ..models.entrega import Entrega
from ..models.curso import Curso
from ..forms import TareaForm, EntregaForm

# Servicio para crear una tarea en un curso
def crear_tarea_service(request, curso_id):
    # Obtiene el curso o retorna un error 404 si no se encuentra
    curso = get_object_or_404(Curso, id=curso_id)
    # Verifica si el usuario es un profesor y es el profesor del curso
    if hasattr(request.user, 'profesor') and curso.profesor == request.user.profesor:
        if request.method == 'POST':
            form = TareaForm(request.POST)
            if form.is_valid():
                tarea = form.save(commit=False)
                tarea.curso = curso  # Asocia la tarea con el curso
                tarea.save()
                return tarea  # Retorna la tarea creada
            else:
                return {'errors': form.errors}
    return {'error': 'Unauthorized'}  # Retorna un error si el usuario no está autorizado

# Servicio para entregar una tarea por parte de un alumno
def entregar_tarea_service(request, tarea_id):
    # Obtiene la tarea o retorna un error 404 si no se encuentra
    tarea = get_object_or_404(Tarea, id=tarea_id)
    # Verifica si el usuario es un alumno
    if hasattr(request.user, 'alumno'):
        if request.method == 'POST':
            form = EntregaForm(request.POST, request.FILES)
            if form.is_valid():
                entrega = form.save(commit=False)
                entrega.tarea = tarea  # Asocia la entrega con la tarea
                entrega.estudiante = request.user.alumno  # Asocia la entrega con el alumno
                entrega.fecha_entrega = timezone.now()  # Marca la fecha de entrega
                entrega.save()
                return {'success': True, 'entrega_id': entrega.id}  # Retorna el ID de la entrega
            else:
                return {'errors': form.errors}
    return {'error': 'Unauthorized'}  # Retorna un error si el usuario no está autorizado

# Servicio para listar todas las tareas de un curso
def lista_tareas_service(request, curso_id):
    # Obtiene el curso o retorna un error 404 si no se encuentra
    curso = get_object_or_404(Curso, id=curso_id)
    # Obtiene todas las tareas asociadas al curso
    tareas = Tarea.objects.filter(curso=curso)
    return {
        'curso_id': curso.id,
        'tareas': [{'id': t.id, 'titulo': t.titulo, 'descripcion': t.descripcion, 'fecha_entrega': t.fecha_entrega} for t in tareas]
    }

# Servicio para obtener detalles de una tarea y gestionar entregas
def tarea_detalle_service(request, tarea_id):
    # Obtiene la tarea o retorna un error 404 si no se encuentra
    tarea = get_object_or_404(Tarea, id=tarea_id)
    # Verifica si el usuario es el profesor del curso asociado a la tarea
    es_profesor = hasattr(request.user, 'profesor') and tarea.curso.profesor == request.user.profesor
    entrega = None
    # Verifica si el usuario es un alumno y obtiene la entrega correspondiente si existe
    if hasattr(request.user, 'alumno'):
        entrega = Entrega.objects.filter(tarea=tarea, estudiante=request.user.alumno).first()

    # Maneja la entrega de la tarea si es una solicitud POST y el usuario no es profesor
    if request.method == 'POST' and not es_profesor:
        form = EntregaForm(request.POST, request.FILES)
        if form.is_valid():
            if entrega:
                entrega.archivo.delete()  # Elimina el archivo anterior si ya existe una entrega
                entrega.archivo = form.cleaned_data['archivo']
                entrega.comentario = form.cleaned_data['comentario']
                entrega.fecha_entrega = timezone.now()
                entrega.save()
            else:
                entrega = Entrega.objects.create(
                    tarea=tarea,
                    estudiante=request.user.alumno,
                    archivo=form.cleaned_data['archivo'],
                    comentario=form.cleaned_data['comentario'],
                    fecha_entrega=timezone.now()
                )
            return {'success': True, 'entrega_id': entrega.id}  # Retorna el ID de la entrega

    return {
        'tarea_id': tarea.id,
        'es_profesor': es_profesor,
        'entrega': {
            'id': entrega.id,
            'archivo': entrega.archivo.url,
            'comentario': entrega.comentario,
            'fecha_entrega': entrega.fecha_entrega
        } if entrega else None
    }
