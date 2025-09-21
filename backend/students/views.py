from rest_framework import viewsets, permissions
from academics.models import AcademicYear
from .models import Student
from .serializers import StudentSerializer


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Par défaut, on affiche uniquement les étudiants
        de l’année académique active.
        """
        active = AcademicYear.objects.filter(is_active=True).first()
        if active:
            return (
                Student.objects
                .filter(academic_year=active)
                .select_related("user", "academic_year")
            )
        return Student.objects.none()
