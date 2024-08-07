from django.shortcuts import get_object_or_404
from django.utils import timezone
from ..models.tarea import Tarea
from ..models.entrega import Entrega
from ..models.curso import Curso
from ..forms import TareaForm, EntregaForm

def crear_tarea_service(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)
    if hasattr(request.user, 'profesor') and curso.profesor == request.user.profesor:
        if request.method == 'POST':
            form = TareaForm(request.POST)
            if form.is_valid():
                tarea = form.save(commit=False)
                tarea.curso = curso
                tarea.save()
                return tarea  # Retornar la tarea creada en lugar de un diccionario
            else:
                return {'errors': form.errors}
    return {'error': 'Unauthorized'}

def entregar_tarea_service(request, tarea_id):
    tarea = get_object_or_404(Tarea, id=tarea_id)
    if hasattr(request.user, 'alumno'):
        if request.method == 'POST':
            form = EntregaForm(request.POST, request.FILES)
            if form.is_valid():
                entrega = form.save(commit=False)
                entrega.tarea = tarea
                entrega.estudiante = request.user.alumno
                entrega.fecha_entrega = timezone.now()
                entrega.save()
                return {'success': True, 'entrega_id': entrega.id}
            else:
                return {'errors': form.errors}
    return {'error': 'Unauthorized'}

def lista_tareas_service(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)
    tareas = Tarea.objects.filter(curso=curso)
    return {
        'curso_id': curso.id,
        'tareas': [{'id': t.id, 'titulo': t.titulo, 'descripcion': t.descripcion, 'fecha_entrega': t.fecha_entrega} for t in tareas]
    }

def tarea_detalle_service(request, tarea_id):
    tarea = get_object_or_404(Tarea, id=tarea_id)
    es_profesor = hasattr(request.user, 'profesor') and tarea.curso.profesor == request.user.profesor
    entrega = None
    if hasattr(request.user, 'alumno'):
        entrega = Entrega.objects.filter(tarea=tarea, estudiante=request.user.alumno).first()

    if request.method == 'POST' and not es_profesor:
        form = EntregaForm(request.POST, request.FILES)
        if form.is_valid():
            if entrega:
                entrega.archivo.delete()
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
            return {'success': True, 'entrega_id': entrega.id}

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
