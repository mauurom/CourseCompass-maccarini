from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from ..models import Curso, Tarea
from ..forms import TareaForm, EntregaForm
from ..services.tarea_service import crear_tarea_service, entregar_tarea_service, tarea_detalle_service

@login_required
def crear_tarea(request, curso_id):
    if request.method == 'POST':
        # Llama al servicio para crear la tarea
        response = crear_tarea_service(request, curso_id)
        if isinstance(response, Tarea):
            # Retorna éxito si la tarea se creó correctamente
            return JsonResponse({'success': True, 'curso_id': curso_id}, status=201)
        else:
            # Retorna errores si algo salió mal
            return JsonResponse(response, status=400)
    else:
        # Si no es POST, muestra el formulario para crear una tarea
        form = TareaForm()
        curso = get_object_or_404(Curso, id=curso_id)
        # Obtiene datos del formulario y del curso
        form_data = {field.name: field.value_from_object(form.instance) for field in form}
        curso_data = {
            'id': curso.id,
            'nombre': curso.nombre,
            'descripcion': curso.descripcion,
            'año': curso.año,
            'horario': curso.horario,
            'profesor_id': curso.profesor.id,
        }
        # Retorna el formulario y datos del curso en formato JSON
        return JsonResponse({'form': form_data, 'curso': curso_data}, status=200)

@login_required
def entregar_tarea(request, tarea_id):
    # Llama al servicio para entregar la tarea
    response = entregar_tarea_service(request, tarea_id)
    if response:
        # Retorna la respuesta del servicio
        return JsonResponse(response, status=200)
    # Mensaje de éxito si la tarea se entregó correctamente
    return JsonResponse({'message': 'Task delivered successfully'}, status=200)

@login_required
def tarea_detalle(request, tarea_id):
    # Obtiene la tarea específica o retorna 404 si no existe
    tarea = get_object_or_404(Tarea, id=tarea_id)
    # Prepara los detalles de la tarea para la respuesta
    context = {
        'titulo': tarea.titulo,
        'descripcion': tarea.descripcion,
        'fecha_entrega': tarea.fecha_entrega,
        'curso': {
            'id': tarea.curso.id,
            'nombre': tarea.curso.nombre,
        }
    }
    # Retorna los detalles de la tarea en formato JSON
    return JsonResponse(context, status=200)
