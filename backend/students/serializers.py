from rest_framework import serializers

from accounts.models import User

from academics.models import AcademicYear
from .models import Student

class StudentSerializer(serializers.ModelSerializer):
    # Pour que le formulaire DRF soit simple à utiliser dans le navigateur
    user = serializers.SlugRelatedField(
        slug_field="username",
        queryset=User.objects.all()
    )
    academic_year = serializers.SlugRelatedField(
        slug_field="name",
        queryset=AcademicYear.objects.all()
    )

    class Meta:
        model = Student
        fields = ["id", "user", "academic_year", "matricule", "program", "date_of_birth", "created_at"]
        read_only_fields = ["created_at"]
