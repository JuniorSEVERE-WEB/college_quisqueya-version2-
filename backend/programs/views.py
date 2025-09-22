from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions

from .models import Program, Classroom, Subject
from .serializers import ProgramSerializer, ClassroomSerializer, SubjectSerializer


class ProgramViewSet(viewsets.ModelViewSet):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer
    permission_classes = [permissions.IsAuthenticated]

    filterset_fields = ["academic_year", "user", "id"]
    search_fields = ["user__username", "user__first_name", "user__last_name", "user__email"]
    ordering_fields = ["id", "user__username"]


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


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [permissions.IsAuthenticated]
