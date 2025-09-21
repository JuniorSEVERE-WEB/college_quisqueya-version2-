from rest_framework import viewsets, permissions
from .models import Employee
from .serializers import EmployeeSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.select_related("user").all()  # si Employee a un FK vers User
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAuthenticated]
