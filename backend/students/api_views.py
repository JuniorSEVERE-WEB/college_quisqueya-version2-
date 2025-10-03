# students/api_views.py
from rest_framework import generics, permissions
from .models import Student
from .serializers_register import StudentRegisterSerializer

class StudentRegisterView(generics.CreateAPIView):
    """
    Endpoint public pour l'inscription des étudiants
    Accessible via: /api/students/register/
    """
    queryset = Student.objects.all()
    serializer_class = StudentRegisterSerializer
    permission_classes = [permissions.AllowAny]   # ouvert à tous
    authentication_classes = []  # pas besoin de JWT pour s’inscrire
