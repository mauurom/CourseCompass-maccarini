from rest_framework import viewsets
from ..models.profesor import Profesor
from ..serializers.profesor_serializer import ProfesorSerializer

class ProfesorViewSet(viewsets.ModelViewSet):
    queryset = Profesor.objects.all()
    serializer_class = ProfesorSerializer
