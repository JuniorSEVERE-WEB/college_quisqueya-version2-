from rest_framework import serializers
from accounts.models import User
from academics.models import AcademicYear
from programs.models import Classroom
from .models import Student

class StudentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role="student"))
    academic_year = serializers.SlugRelatedField(slug_field="name", queryset=AcademicYear.objects.all())
    classroom = serializers.PrimaryKeyRelatedField(queryset=Classroom.objects.all())
    classroom_label = serializers.CharField(source="classroom.name", read_only=True)

    birth_certificate = serializers.FileField(required=False, allow_null=True, help_text="PDF uniquement, max 3MB")
    last_school_report = serializers.FileField(required=False, allow_null=True, help_text="PDF uniquement, max 3MB")

    class Meta:
        model = Student
        fields = [
            "id", "user", "academic_year", "classroom", "classroom_label", "matricule", "date_of_birth", "created_at",
            "birth_certificate", "last_school_report"
        ]
        read_only_fields = ["created_at"]

    def validate_birth_certificate(self, file):
        if file:
            if file.size > 3 * 1024 * 1024:
                raise serializers.ValidationError("Le fichier ne doit pas dépasser 3 MB.")
            if not file.name.lower().endswith('.pdf'):
                raise serializers.ValidationError("Le fichier doit être au format PDF.")
        return file

    def validate_last_school_report(self, file):
        if file:
            if file.size > 3 * 1024 * 1024:
                raise serializers.ValidationError("Le fichier ne doit pas dépasser 3 MB.")
            if not file.name.lower().endswith('.pdf'):
                raise serializers.ValidationError("Le fichier doit être au format PDF.")
        return file
