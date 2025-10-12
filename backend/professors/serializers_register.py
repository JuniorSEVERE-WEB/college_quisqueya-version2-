# professors/serializers_register.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from academics.models import AcademicYear
from programs.models import Program, Subject
from .models import Professor

User = get_user_model()


class ProfessorRegisterSerializer(serializers.ModelSerializer):
    # Champs User
    username = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)

    # 🔹 Champs facultatifs
    phone = serializers.CharField(required=False, allow_blank=True)
    sexe = serializers.ChoiceField(choices=User.SEXE_CHOICES, required=False, allow_blank=True)

    # Champs Professeur
    program = serializers.PrimaryKeyRelatedField(
        queryset=Program.objects.all(),
        required=True
    )
    subjects = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Subject.objects.all(),
        required=True
    )

    class Meta:
        model = Professor
        fields = [
            "username", "email", "password1", "password2",
            "first_name", "last_name", "sexe", "phone",
            "department", "hire_date", "program", "subjects",
        ]

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Ce nom d’utilisateur existe déjà.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Cet email est déjà utilisé.")
        return value

    def validate(self, attrs):
        if attrs["password1"] != attrs["password2"]:
            raise serializers.ValidationError("Les mots de passe ne correspondent pas.")
        return attrs

    def create(self, validated_data):
        username = validated_data.pop("username")
        email = validated_data.pop("email")
        password = validated_data.pop("password1")
        validated_data.pop("password2", None)
        first_name = validated_data.pop("first_name")
        last_name = validated_data.pop("last_name")
        sexe = validated_data.pop("sexe", "")
        phone = validated_data.pop("phone", "")

        # Créer l'utilisateur
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            sexe=sexe,
            phone=phone,
            role="prof",
            is_active=False,
        )

        active_year = AcademicYear.objects.filter(is_active=True).first()
        if not active_year:
            raise serializers.ValidationError("Aucune année académique active.")

        subjects = validated_data.pop("subjects", [])
        program = validated_data.pop("program")

        professor = Professor.objects.create(
            user=user,
            academic_year=active_year,
            program=program,
            **validated_data
        )
        professor.subjects.set(subjects)
        return professor
