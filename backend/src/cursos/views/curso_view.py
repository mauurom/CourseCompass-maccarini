from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from ..services.curso_service import curso_detalle_service, lista_cursos_service, crear_curso_service

@login_required
def curso_detalle(request, curso_id):
    context = curso_detalle_service(request, curso_id)
    return render(request, 'cursos/curso_detalle.html', context)

@login_required
def lista_cursos(request):
    context = lista_cursos_service(request)
    return render(request, 'cursos/lista_cursos.html', context)

@login_required
def crear_curso(request):
    response = crear_curso_service(request)
    if response:
        return response
    return render(request, 'cursos/crear_curso.html')
