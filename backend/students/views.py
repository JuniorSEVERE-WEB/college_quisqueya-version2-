from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions
from academics.models import AcademicYear
from .models import Student
from .serializers import StudentSerializer

class StudentViewSet(viewsets.ModelViewSet):
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Par défaut, on affiche les étudiants de l’année active (visible dans le navigateur)
        active = AcademicYear.objects.filter(is_active=True).first()
        if active:
            return Student.objects.filter(academic_year=active).select_related("user", "academic_year")
        return Student.objects.none()
