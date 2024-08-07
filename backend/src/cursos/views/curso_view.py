from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from ..services.curso_service import curso_detalle_service, lista_cursos_service, crear_curso_service

@login_required
def curso_detalle(request, curso_id):
    context = curso_detalle_service(request, curso_id)
    return JsonResponse(context, status=200)

@login_required
def lista_cursos(request):
    context = lista_cursos_service(request)
    return JsonResponse(context, status=200)

@login_required
def crear_curso(request):
    response = crear_curso_service(request)
    if isinstance(response, dict):
        return JsonResponse(response, status=201)
    else:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
