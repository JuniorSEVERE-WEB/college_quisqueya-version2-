# programs/views.py
from rest_framework import viewsets, permissions
from .models import Program, Classroom, Subject
from .serializers import ProgramSerializer, ClassroomSerializer, SubjectSerializer


class ProgramViewSet(viewsets.ModelViewSet):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer
    permission_classes = [permissions.IsAuthenticated]


class ClassroomViewSet(viewsets.ReadOnlyModelViewSet):
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
