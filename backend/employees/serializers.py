from rest_framework import serializers
from accounts.models import User
from academics.models import AcademicYear
from .models import Employee

class EmployeeSerializer(serializers.ModelSerializer):
    def validate_user(self, value):
        from .models import Employee
        if Employee.objects.filter(user=value).exists():
            raise serializers.ValidationError("This user is already assigned to an employee.")
        return value
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role="employee")  # seuls les users role=employee
    )
    academic_year = serializers.SlugRelatedField(
        slug_field="name",
        queryset=AcademicYear.objects.all()
    )

    class Meta:
        model = Employee
        fields = ["id", "user", "academic_year", "position", "hire_date", "created_at"]
        read_only_fields = ["created_at"]
