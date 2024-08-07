from django.shortcuts import get_object_or_404
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
            return {'success': True, 'message': 'Inscripción realizada'}

    inscripciones = None
    if es_profesor:
        inscripciones = InscripcionMateria.objects.filter(curso=curso)

    return {
        'curso': {
            'id': curso.id,
            'nombre': curso.nombre,
            'descripcion': curso.descripcion,
            'año': curso.año,
            'horario': curso.horario,
            'profesor_id': curso.profesor.id
        },
        'inscrito': inscrito,
        'es_profesor': es_profesor,
        'inscripciones': [{'estudiante_id': i.estudiante.id, 'fecha_inscripcion': i.fecha_inscripcion} for i in inscripciones] if inscripciones else []
    }

def lista_cursos_service(request):
    usuario = request.user
    materias = Curso.objects.all()
    inscripciones = InscripcionMateria.objects.filter(estudiante__usuario=usuario) if hasattr(usuario, 'alumno') else None

    # Determinar el tipo de usuario
    if hasattr(usuario, 'profesor'):
        tipo_usuario = 'profesor'
    elif hasattr(usuario, 'alumno'):
        tipo_usuario = 'alumno'
    else:
        tipo_usuario = 'desconocido'

    return {
        'user_id': usuario.id,
        'asignaturas': [{'id': m.id, 'nombre': m.nombre, 'descripcion': m.descripcion, 'año': m.año, 'horario': m.horario} for m in materias],
        'inscripciones': [{'curso_id': i.curso.id, 'fecha_inscripcion': i.fecha_inscripcion} for i in inscripciones] if inscripciones else [],
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
            curso = Curso.objects.create(
                nombre=nombre,
                descripcion=descripcion,
                año=año,
                horario=horario,
                contraseña_matriculacion=contraseña_matriculacion,
                profesor=profesor
            )
            return {'curso_id': curso.id, 'success': True}
    else:
        return {'error': 'Unauthorized'}
