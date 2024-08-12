from rest_framework import viewsets
from ..models.alumno import Alumno
from ..serializers.alumno_serializer import AlumnoSerializer
#Vista de Alumno 
class AlumnoViewSet(viewsets.ModelViewSet):
    queryset = Alumno.objects.all()
    serializer_class = AlumnoSerializer
