from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import Program, Classroom
from .serializers import ProgramSerializer, ClassroomSerializer

class ProgramViewSet(viewsets.ModelViewSet):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer

class ClassroomViewSet(viewsets.ReadOnlyModelViewSet):
    """
    On permet de filtrer par paramètre ?program=<id>
    Exemple: /api/classrooms/?program=5
    """
    serializer_class = ClassroomSerializer

    def get_queryset(self):
        qs = Classroom.objects.select_related("program").all()
        program = self.request.query_params.get("program")
        if program:
            qs = qs.filter(program_id=program)
        return qs

