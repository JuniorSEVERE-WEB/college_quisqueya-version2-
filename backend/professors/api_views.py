# professors/api_views.py
from rest_framework import generics, permissions
from .serializers_register import ProfessorRegisterSerializer
from .models import Professor

class ProfessorRegisterView(generics.CreateAPIView):
    """
    Endpoint public pour l'inscription des professeurs
    Accessible via: /api/professors/register/
    """
    queryset = Professor.objects.all()
    serializer_class = ProfessorRegisterSerializer
    permission_classes = [permissions.AllowAny]   # inscription ouverte
    authentication_classes = []  # pas besoin de JWT
