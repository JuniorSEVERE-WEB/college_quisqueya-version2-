from rest_framework import serializers
from accounts.models import User
from academics.models import AcademicYear
from programs.models import Classroom
from .models import Student


class UserNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email", "sexe", "phone"]


class StudentSerializer(serializers.ModelSerializer):
    user = UserNestedSerializer(read_only=True)
    academic_year = serializers.SlugRelatedField(
        slug_field="name",
        queryset=AcademicYear.objects.all()
    )
    classroom = serializers.PrimaryKeyRelatedField(
        queryset=Classroom.objects.all()
    )
    classroom_label = serializers.CharField(
        source="classroom.name",
        read_only=True
    )

    # ✅ Assure-toi que ces champs sont inclus :
    father_job = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    mother_job = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    birth_certificate = serializers.FileField(required=False, allow_null=True)
    last_school_report = serializers.FileField(required=False, allow_null=True)

    class Meta:
        model = Student
        fields = "__all__"
