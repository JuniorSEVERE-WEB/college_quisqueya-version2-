from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import ReportSession, SubjectCoefficient, Grade
from .serializers import (
    ReportSessionSerializer,
    SubjectCoefficientSerializer,
    GradeSerializer,
)


class ReportSessionViewSet(viewsets.ModelViewSet):
    queryset = ReportSession.objects.select_related("classroom", "academic_year", "created_by").all()
    serializer_class = ReportSessionSerializer
    permission_classes = [permissions.IsAuthenticated]
    ordering = ["-created_at"]

    # Ajout DRF filters
    filterset_fields = ["classroom", "academic_year", "is_active", "trimester", "step"]
    ordering_fields = ["created_at", "id"]

    def get_queryset(self):
        qs = super().get_queryset()
        # Filtres manuels
        classroom_id = self.request.query_params.get("classroom")
        ay_id = self.request.query_params.get("academic_year")
        active = self.request.query_params.get("active")
        if classroom_id:
            qs = qs.filter(classroom_id=classroom_id)
        if ay_id:
            qs = qs.filter(academic_year_id=ay_id)
        if active in {"1", "true", "True"}:
            qs = qs.filter(is_active=True)
        return qs

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=["post"])
    def activate(self, request, pk=None):
        session = self.get_object()
        ReportSession.objects.filter(is_active=True).exclude(pk=session.pk).update(is_active=False)
        session.is_active = True
        session.save()
        return Response({"status": "activated"}, status=status.HTTP_200_OK)


class SubjectCoefficientViewSet(viewsets.ModelViewSet):
    queryset = SubjectCoefficient.objects.select_related("classroom", "subject", "academic_year").all()
    serializer_class = SubjectCoefficientSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Ajout DRF filters
    filterset_fields = ["classroom", "subject", "academic_year"]
    ordering_fields = ["coefficient", "id"]

    def get_queryset(self):
        qs = super().get_queryset()
        # Filtres manuels
        classroom_id = self.request.query_params.get("classroom")
        subject_id = self.request.query_params.get("subject")
        ay_id = self.request.query_params.get("academic_year")
        if classroom_id:
            qs = qs.filter(classroom_id=classroom_id)
        if subject_id:
            qs = qs.filter(subject_id=subject_id)
        if ay_id:
            qs = qs.filter(academic_year_id=ay_id)
        return qs


class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.select_related(
        "program", "classroom", "student", "subject", "report_session"
    ).all()
    serializer_class = GradeSerializer
    permission_classes = [permissions.IsAuthenticated]
    ordering = ["student_id", "subject_id"]

    # Ajout DRF filters
    filterset_fields = ["student", "classroom", "subject", "program", "report_session"]
    ordering_fields = ["student", "subject", "note", "id"]

    def get_queryset(self):
        qs = super().get_queryset()
        # Filtres manuels
        student_id = self.request.query_params.get("student")
        classroom_id = self.request.query_params.get("classroom")
        subject_id = self.request.query_params.get("subject")
        program_id = self.request.query_params.get("program")
        session_id = self.request.query_params.get("report_session")
        ay_id = self.request.query_params.get("academic_year")

        if student_id:
            qs = qs.filter(student_id=student_id)
        if classroom_id:
            qs = qs.filter(classroom_id=classroom_id)
        if subject_id:
            qs = qs.filter(subject_id=subject_id)
        if program_id:
            qs = qs.filter(program_id=program_id)
        if session_id:
            qs = qs.filter(report_session_id=session_id)
        if ay_id:
            qs = qs.filter(report_session__academic_year_id=ay_id)
        return qs
