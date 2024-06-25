from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from ..models.curso import Curso
from ..models.inscripcion import InscripcionMateria

def curso_detalle_service(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)
    es_profesor = hasattr(request.user, 'profesor') and curso.profesor == request.user.profesor
    inscrito = False

    if hasattr(request.user, 'alumno'):
        inscrito = InscripcionMateria.objects.filter(estudiante=request.user.alumno, curso=curso).exists()

    if request.method == 'POST' and 'contraseña_matriculacion' in request.POST and not es_profesor:
        if request.POST['contraseña_matriculacion'] == curso.contraseña_matriculacion:
            InscripcionMateria.objects.create(
                estudiante=request.user.alumno,
                curso=curso,
                fecha_inscripcion=timezone.now()
            )
            return redirect('lista_cursos')

    inscripciones = None
    if es_profesor:
        inscripciones = InscripcionMateria.objects.filter(curso=curso)

    return {
        'curso': curso,
        'inscrito': inscrito,
        'es_profesor': es_profesor,
        'inscripciones': inscripciones,
    }

def lista_cursos_service(request):
    usuario = request.user
    materias = Curso.objects.all()
    inscripciones = InscripcionMateria.objects.filter(estudiante__usuario=usuario) if hasattr(usuario, 'estudiante') else None

    # Determinar el tipo de usuario
    if hasattr(usuario, 'profesor'):
        tipo_usuario = 'profesor'
    elif hasattr(usuario, 'estudiante'):
        tipo_usuario = 'estudiante'
    else:
        tipo_usuario = 'desconocido'

    return {
        'user': usuario,
        'asignaturas': materias,
        'inscripciones': inscripciones,
        'tipo_usuario': tipo_usuario
    }

def crear_curso_service(request):
    if hasattr(request.user, 'profesor'):
        if request.method == 'POST':
            nombre = request.POST['nombre']
            descripcion = request.POST['descripcion']
            año = request.POST['año']
            horario = request.POST['horario']
            contraseña_matriculacion = request.POST['contraseña_matriculacion']
            profesor = request.user.profesor
            Curso.objects.create(
                nombre=nombre,
                descripcion=descripcion,
                año=año,
                horario=horario,
                contraseña_matriculacion=contraseña_matriculacion,
                profesor=profesor
            )
            return redirect('lista_cursos')
    else:
        return render(request, 'cursos/error.html', {'message': 'Debe ser profesor para crear un curso.'})
