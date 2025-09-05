from rest_framework import viewsets, permissions
from academics.models import AcademicYear
from .models import Professor
from .serializers import ProfessorSerializer

class ProfessorViewSet(viewsets.ModelViewSet):
    serializer_class = ProfessorSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        active = AcademicYear.objects.filter(is_active=True).first()
        if active:
            return Professor.objects.filter(academic_year=active).select_related("user", "academic_year")
        return Professor.objects.none()
