# employees/api_views.py
from rest_framework import generics, permissions
from .models import Employee
from .serializers_register import EmployeeRegisterSerializer

class EmployeeRegisterView(generics.CreateAPIView):
    """
    Endpoint public pour l'inscription des employés
    Accessible via: /api/employees/register/
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeRegisterSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = []  # inscription ouverte
