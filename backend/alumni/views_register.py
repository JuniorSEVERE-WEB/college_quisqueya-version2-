# alumni/views_register.py
from rest_framework import generics, permissions
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from .models import Alumni
from .serializers_register import AlumniRegisterSerializer


class AlumniRegisterAPIView(generics.CreateAPIView):
    """
    Endpoint public pour inscription des Alumni
    """
    queryset = Alumni.objects.all()
    serializer_class = AlumniRegisterSerializer
    permission_classes = [permissions.AllowAny]  # ✅ PUBLIC
    parser_classes = [MultiPartParser, FormParser, JSONParser]
