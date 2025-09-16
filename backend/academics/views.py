from rest_framework import viewsets, permissions

from professors import serializers
from .models import (
    AcademicYear, Trimester, Step, Classroom, Subject,
    Professor, Student, Note, Resource, Assignment, Submission
)
from .serializers import (
    AcademicYearSerializer, TrimesterSerializer, StepSerializer, ClassroomSerializer, SubjectSerializer,
    ProfessorSerializer, StudentSerializer, NoteSerializer, ResourceSerializer, AssignmentSerializer, SubmissionSerializer
)
from .permissions import IsAdminOrReadOnly, IsProfessorOrAdmin, IsStudentOrAdmin
from rest_framework.decorators import action
from rest_framework.response import Response

class AcademicYearViewSet(viewsets.ModelViewSet):
    queryset = AcademicYear.objects.all()
    serializer_class = AcademicYearSerializer
    permission_classes = [permissions.IsAdminUser]

class TrimesterViewSet(viewsets.ModelViewSet):
    queryset = Trimester.objects.all()
    serializer_class = TrimesterSerializer
    permission_classes = [permissions.IsAdminUser]

class StepViewSet(viewsets.ModelViewSet):
    queryset = Step.objects.all()
    serializer_class = StepSerializer
    permission_classes = [permissions.IsAdminUser]

class ClassroomViewSet(viewsets.ModelViewSet):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer
    permission_classes = [permissions.IsAdminUser]

class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [permissions.IsAdminUser]

class ProfessorViewSet(viewsets.ModelViewSet):
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer
    permission_classes = [permissions.IsAdminUser]

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAdminUser]

    def moyenne_etape(self, step):
        notes = self.notes.filter(step=step)
        total = 0
        total_coeff = 0
        for note in notes:
            coeff = note.subject.coefficient
            total += note.value * coeff
            total_coeff += coeff
        return total / total_coeff if total_coeff > 0 else None

    def moyenne_annuelle(self):
        steps = Step.objects.filter(trimester__academic_year=self.classroom.academic_year)
        moyennes = [self.moyenne_etape(step) for step in steps if self.moyenne_etape(step) is not None]
        return sum(moyennes) / len(moyennes) if moyennes else None
    
    @action(detail=True, methods=["get"], url_path="moyennes")
    def get_moyennes(self, request, pk=None):
        student = self.get_object()
        steps = Step.objects.filter(trimester__academic_year=student.classroom.academic_year)
        moyennes = {
            step.name: student.moyenne_etape(step) for step in steps
        }
        moyenne_annuelle = student.moyenne_annuelle()
        return Response({
            "moyennes_par_etape": moyennes,
            "moyenne_annuelle": moyenne_annuelle
        })

class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [IsProfessorOrAdmin]

    def perform_create(self, serializer):
        step = serializer.validated_data.get("step")
        if not step.is_active:
            raise serializers.ValidationError("Impossible de modifier une étape non active.")
        serializer.save()

    def perform_update(self, serializer):
        step = serializer.validated_data.get("step")
        if not step.is_active:
            raise serializers.ValidationError("Impossible de modifier une étape non active.")
        serializer.save()

class ResourceViewSet(viewsets.ModelViewSet):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    permission_classes = [IsProfessorOrAdmin]

    def perform_create(self, serializer):
        step = serializer.validated_data.get("step")
        if not step.is_active:
            raise serializers.ValidationError("Impossible de modifier une étape non active.")
        serializer.save()

    def perform_update(self, serializer):
        step = serializer.validated_data.get("step")
        if not step.is_active:
            raise serializers.ValidationError("Impossible de modifier une étape non active.")
        serializer.save()

class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [IsProfessorOrAdmin]

    def perform_create(self, serializer):
        step = serializer.validated_data.get("step")
        if not step.is_active:
            raise serializers.ValidationError("Impossible de modifier une étape non active.")
        serializer.save()

    def perform_update(self, serializer):
        step = serializer.validated_data.get("step")
        if not step.is_active:
            raise serializers.ValidationError("Impossible de modifier une étape non active.")
        serializer.save()

class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = [IsStudentOrAdmin]

    def perform_create(self, serializer):
        step = serializer.validated_data.get("assignment").step
        if not step.is_active:
            raise serializers.ValidationError("Impossible de soumettre un devoir pour une étape non active.")
        serializer.save()

    def perform_update(self, serializer):
        step = serializer.validated_data.get("assignment").step
        if not step.is_active:
            raise serializers.ValidationError("Impossible de modifier une soumission pour une étape non active.")
        serializer.save()