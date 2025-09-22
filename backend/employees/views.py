from rest_framework import viewsets, permissions
from .models import Employee
from .serializers import EmployeeSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.select_related("user").all()  # si Employee a un FK vers User
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Filtres/Recherche/Tri
    filterset_fields = ["student", "amount", "id"]
    search_fields = ["student__username", "student__email"]
    ordering_fields = ["id", "amount"]
