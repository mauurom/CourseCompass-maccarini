from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from ..models import Curso, Tarea
from ..forms import TareaForm, EntregaForm
from ..services.tarea_service import crear_tarea_service, entregar_tarea_service, tarea_detalle_service

@login_required
def crear_tarea(request, curso_id):
    if request.method == 'POST':
        response = crear_tarea_service(request, curso_id)
        if isinstance(response, Tarea):
            return JsonResponse({'success': True, 'curso_id': curso_id}, status=201)
        else:
            return JsonResponse(response, status=400)
    else:
        form = TareaForm()
        curso = get_object_or_404(Curso, id=curso_id)
        form_data = {field.name: field.value_from_object(form.instance) for field in form}
        curso_data = {
            'id': curso.id,
            'nombre': curso.nombre,
            'descripcion': curso.descripcion,
            'año': curso.año,
            'horario': curso.horario,
            'profesor_id': curso.profesor.id,
        }
        return JsonResponse({'form': form_data, 'curso': curso_data}, status=200)

@login_required
def entregar_tarea(request, tarea_id):
    response = entregar_tarea_service(request, tarea_id)
    if response:
        return JsonResponse(response, status=200)
    return JsonResponse({'message': 'Task delivered successfully'}, status=200)

@login_required
def tarea_detalle(request, tarea_id):
    tarea = get_object_or_404(Tarea, id=tarea_id)
    context = {
        'titulo': tarea.titulo,
        'descripcion': tarea.descripcion,
        'fecha_entrega': tarea.fecha_entrega,
        'curso': {
            'id': tarea.curso.id,
            'nombre': tarea.curso.nombre,
        }
    }
    return JsonResponse(context, status=200)