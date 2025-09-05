from rest_framework import serializers
from academics.models import AcademicYear
from accounts.models import User
from .models import Professor

class ProfessorSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role="prof")  # on limite aux utilisateurs rôle "professeur"
    )
    academic_year = serializers.SlugRelatedField(
        slug_field="name",
        queryset=AcademicYear.objects.all()
    )

    class Meta:
        model = Professor
        fields = ["id", "user", "academic_year", "department", "hire_date", "created_at"]
        read_only_fields = ["created_at"]
