from django.shortcuts import get_object_or_404, redirect
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
                return redirect('curso_detalle', curso_id=curso.id)
        else:
            form = TareaForm()
        return {'form': form, 'curso': curso}

def entregar_tarea_service(request, tarea_id):
    tarea = get_object_or_404(Tarea, id=tarea_id)
    if hasattr(request.user, 'estudiante'):
        if request.method == 'POST':
            form = EntregaForm(request.POST, request.FILES)
            if form.is_valid():
                entrega = form.save(commit=False)
                entrega.tarea = tarea
                entrega.estudiante = request.user.estudiante
                entrega.fecha_entrega = timezone.now()
                entrega.save()
                return redirect('curso_detalle', curso_id=tarea.curso.id)
        else:
            form = EntregaForm()
        return {'form': form, 'tarea': tarea}

def lista_tareas_service(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)
    tareas = Tarea.objects.filter(curso=curso)
    return {
        'curso': curso,
        'tareas': tareas
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
                Entrega.objects.create(
                    tarea=tarea,
                    estudiante=request.user.alumno,
                    archivo=form.cleaned_data['archivo'],
                    comentario=form.cleaned_data['comentario'],
                    fecha_entrega=timezone.now()
                )
            return redirect('tarea_detalle', tarea_id=tarea.id)
    else:
        form = EntregaForm()

    return {
        'tarea': tarea,
        'es_profesor': es_profesor,
        'form': form,
        'entrega': entrega
    }
