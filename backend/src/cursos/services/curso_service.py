from django.shortcuts import get_object_or_404
from django.utils import timezone
from ..models.curso import Curso
from ..models.inscripcion import InscripcionMateria

#Servicio para obtener detalles de un curso y gestionar inscripciones
def curso_detalle_service(request, curso_id):
    #Obtiene el curso o retorna un error 404 si no se encuentra
    curso = get_object_or_404(Curso, id=curso_id)
    #Verifica si el usuario es el profesor del curso
    es_profesor = hasattr(request.user, 'profesor') and curso.profesor == request.user.profesor
    inscrito = False

    #Verifica si el usuario es un alumno y si está inscrito en el curso
    if hasattr(request.user, 'alumno'):
        inscrito = InscripcionMateria.objects.filter(estudiante=request.user.alumno, curso=curso).exists()

    #Maneja la inscripción del alumno al curso si es una solicitud POST y el usuario no es profesor
    if request.method == 'POST' and 'contraseña_matriculacion' in request.POST and not es_profesor:
        if request.POST['contraseña_matriculacion'] == curso.contraseña_matriculacion:
            InscripcionMateria.objects.create(
                estudiante=request.user.alumno,
                curso=curso,
                fecha_inscripcion=timezone.now()
            )
            return {'success': True, 'message': 'Inscripción realizada'}

    inscripciones = None
    #Si el usuario es profesor, obtiene las inscripciones del curso
    if es_profesor:
        inscripciones = InscripcionMateria.objects.filter(curso=curso)

    return {
        'curso': {
            'id': curso.id,
            'nombre': curso.nombre,
            'descripcion': curso.descripcion,
            'año': curso.año,
            'horario': curso.horario,
            'profesor_id': curso.profesor.usuario.id  #Ajuste aquí para obtener el ID del profesor
        },
        'inscrito': inscrito,
        'es_profesor': es_profesor,
        'inscripciones': [{'estudiante_id': i.estudiante.usuario.id, 'fecha_inscripcion': i.fecha_inscripcion} for i in inscripciones] if inscripciones else []
    }

#Servicio para listar todos los cursos y las inscripciones del usuario
def lista_cursos_service(request):
    usuario = request.user
    materias = Curso.objects.all()
    inscripciones = InscripcionMateria.objects.filter(estudiante__usuario=usuario) if hasattr(usuario, 'alumno') else None

    #Determina el tipo de usuario basado en su rol
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

# Servicio para crear un nuevo curso por parte de un profesor
def crear_curso_service(request):
    if hasattr(request.user, 'profesor'):       #Verifica si el usuario es un profesor
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
        return {'error': 'Unauthorized'}                   #Retorna un error si el usuario no es autorizado
