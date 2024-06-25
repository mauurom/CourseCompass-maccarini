from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from ..models import Curso
from ..forms import TareaForm, EntregaForm
from ..services.tarea_service import crear_tarea_service, entregar_tarea_service, tarea_detalle_service

@login_required
def crear_tarea(request, curso_id):
    if request.method == 'POST':
        response = crear_tarea_service(request, curso_id)
        if isinstance(response, dict):
            return render(request, 'cursos/crear_tarea.html', response)
        else:
            return redirect(reverse('curso_detalle', kwargs={'curso_id': curso_id}))
    else:
        form = TareaForm()
        curso = get_object_or_404(Curso, id=curso_id)
        return render(request, 'cursos/crear_tarea.html', {'form': form, 'curso': curso})

@login_required
def entregar_tarea(request, tarea_id):
    response = entregar_tarea_service(request, tarea_id)
    if response:
        return response
    return render(request, 'cursos/entregar_tarea.html')

@login_required
def tarea_detalle(request, tarea_id):
    context = tarea_detalle_service(request, tarea_id)
    return render(request, 'cursos/tarea_detalle.html', context)
