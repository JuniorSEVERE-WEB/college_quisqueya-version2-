from rest_framework import viewsets, permissions, serializers
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import (
    AcademicYear, Trimester, Step, Classroom, Subject,
    Professor, Student, Note, Resource, Assignment, Submission
)
from .serializers import (
    AcademicYearSerializer, TrimesterSerializer, StepSerializer, ClassroomSerializer, SubjectSerializer,
    ProfessorSerializer, StudentSerializer, NoteSerializer, ResourceSerializer, AssignmentSerializer, SubmissionSerializer
)
from .permissions import IsAdminOrReadOnly, IsProfessorOrAdmin, IsStudentOrAdmin


class AcademicYearViewSet(viewsets.ModelViewSet):
    queryset = AcademicYear.objects.all()
    serializer_class = AcademicYearSerializer
    permission_classes = [permissions.IsAdminUser]

    # Filtres/Recherche/Tri
    filterset_fields = ["is_active", "id"]
    ordering_fields = ["id"]


class TrimesterViewSet(viewsets.ModelViewSet):
    queryset = Trimester.objects.all()
    serializer_class = TrimesterSerializer
    permission_classes = [permissions.IsAdminUser]

    # Filtres/Recherche/Tri
    filterset_fields = ["academic_year", "id"]
    ordering_fields = ["id"]


class StepViewSet(viewsets.ModelViewSet):
    queryset = Step.objects.all()
    serializer_class = StepSerializer
    permission_classes = [permissions.IsAdminUser]

    # Filtres/Recherche/Tri
    filterset_fields = ["trimester", "is_active", "id"]
    ordering_fields = ["id"]


class ClassroomViewSet(viewsets.ModelViewSet):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer
    permission_classes = [permissions.IsAdminUser]

    # Filtres/Recherche/Tri
    filterset_fields = ["academic_year", "id"]
    search_fields = ["name"]
    ordering_fields = ["id", "name"]


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [permissions.IsAdminUser]

    filterset_fields = ["classroom", "id"]
    search_fields = ["name"]
    ordering_fields = ["id", "name"]


class ProfessorViewSet(viewsets.ModelViewSet):
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer
    permission_classes = [permissions.IsAdminUser]

    # Filtres/Recherche/Tri
    filterset_fields = ["academic_year", "user", "id"]
    search_fields = ["user__username", "user__first_name", "user__last_name", "user__email"]
    ordering_fields = ["id", "user__username"]


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAdminUser]

    filterset_fields = ["academic_year", "user", "id"]
    search_fields = ["user__username", "user__first_name", "user__last_name", "user__email"]
    ordering_fields = ["id", "user__username"]

    @action(detail=True, methods=["get"], url_path="moyennes")
    def get_moyennes(self, request, pk=None):
        """
        Retourne les moyennes par étape et la moyenne annuelle d’un étudiant
        """
        student = self.get_object()
        steps = Step.objects.filter(trimester__academic_year=student.classroom.academic_year)
        moyennes = {
            step.name: student.moyenne_etape(step) for step in steps
        }
        return Response({
            "moyennes_par_etape": moyennes,
            "moyenne_annuelle": student.moyenne_annuelle()
        })


class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [IsProfessorOrAdmin]

    filterset_fields = ["student", "subject", "step"]
    search_fields = ["student__user__username", "subject__name"]
    ordering_fields = ["value", "id"]

    def _check_step_active(self, serializer):
        step = serializer.validated_data.get("step")
        if not step.is_active:
            raise serializers.ValidationError("Impossible de modifier une étape non active.")
        serializer.save()

    def perform_create(self, serializer):
        self._check_step_active(serializer)

    def perform_update(self, serializer):
        self._check_step_active(serializer)


class ResourceViewSet(viewsets.ModelViewSet):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    permission_classes = [IsProfessorOrAdmin]

    filterset_fields = ["step", "subject", "id"]
    search_fields = ["title"]
    ordering_fields = ["id"]

    def _check_step_active(self, serializer):
        step = serializer.validated_data.get("step")
        if not step.is_active:
            raise serializers.ValidationError("Impossible de modifier une étape non active.")
        serializer.save()

    def perform_create(self, serializer):
        self._check_step_active(serializer)

    def perform_update(self, serializer):
        self._check_step_active(serializer)


class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [IsProfessorOrAdmin]

    filterset_fields = ["step", "subject", "id"]
    search_fields = ["title", "instructions"]
    ordering_fields = ["id"]

    def _check_step_active(self, serializer):
        step = serializer.validated_data.get("step")
        if not step.is_active:
            raise serializers.ValidationError("Impossible de modifier une étape non active.")
        serializer.save()

    def perform_create(self, serializer):
        self._check_step_active(serializer)

    def perform_update(self, serializer):
        self._check_step_active(serializer)


class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = [IsStudentOrAdmin]

    # Filtres/Recherche/Tri
    filterset_fields = ["assignment", "student", "id"]
    ordering_fields = ["id"]

    def _check_step_active(self, serializer):
        step = serializer.validated_data.get("assignment").step
        if not step.is_active:
            raise serializers.ValidationError("Impossible de soumettre/modifier une étape non active.")
        serializer.save()

    def perform_create(self, serializer):
        self._check_step_active(serializer)

    def perform_update(self, serializer):
        self._check_step_active(serializer)
