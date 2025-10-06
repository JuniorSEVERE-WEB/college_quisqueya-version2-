from rest_framework import serializers
from academics.models import AcademicYear
from accounts.models import User
from programs.models import Subject
from .models import Professor


# 🔹 Serializer imbriqué pour l'utilisateur
class UserNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email", "sexe"]


# 🔹 Serializer principal
class ProfessorSerializer(serializers.ModelSerializer):
    user = UserNestedSerializer(read_only=True)
    academic_year = serializers.SlugRelatedField(
        slug_field="name",
        queryset=AcademicYear.objects.all()
    )
    subjects = serializers.SlugRelatedField(
        slug_field="name", queryset=Subject.objects.all(), many=True
    )  # ✅ renvoie les noms des matières

    class Meta:
        model = Professor
        fields = "__all__"
        read_only_fields = ["created_at"]
