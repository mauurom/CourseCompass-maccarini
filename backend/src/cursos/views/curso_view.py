from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from ..services.curso_service import curso_detalle_service, lista_cursos_service, crear_curso_service

@login_required
def curso_detalle(request, curso_id):      
    context = curso_detalle_service(request, curso_id)#Obtiene la información detallada del curso usando el servicio
    return JsonResponse(context, status=200)        #Devuelve una respuesta JSON con el contexto del curso

@login_required
def lista_cursos(request):
    context = lista_cursos_service(request)         #Obtiene la lista de cursos usando el servicio
    return JsonResponse(context, status=200)        #Devuelve una respuesta JSON con la lista de cursos

@login_required
def crear_curso(request):
    # Crea un nuevo curso usando el servicio
    response = crear_curso_service(request)
    if isinstance(response, dict):
        #Si la respuesta es un diccionario (indicando éxito o error)
        #Devuelve una respuesta JSON con el contenido de la respuesta
        return JsonResponse(response, status=201)
    else:
        #Si la respuesta no es un diccionario, se considera no autorizado
        return JsonResponse({'error': 'Unauthorized'}, status=403)
