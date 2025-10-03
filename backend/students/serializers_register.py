# students/serializers_register.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from academics.models import AcademicYear
from programs.models import Classroom
from .models import Student

User = get_user_model()


class StudentRegisterSerializer(serializers.ModelSerializer):
    # Champs User
    username = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    # 🔹 Nouveau champ obligatoire
    sexe = serializers.ChoiceField(choices=User.SEXE_CHOICES, required=True)

    # Champs Student
    classroom = serializers.PrimaryKeyRelatedField(
        queryset=Classroom.objects.all(),
        required=True
    )
    birth_certificate = serializers.FileField(
        required=False, allow_null=True,
        help_text="PDF uniquement, max 3MB"
    )
    last_school_report = serializers.FileField(
        required=False, allow_null=True,
        help_text="PDF uniquement, max 3MB"
    )

    class Meta:
        model = Student
        fields = [
            # Champs User
            "username", "email", "password1", "password2",
            "first_name", "last_name", "sexe",
            # Champs Student
            "classroom", "birth_certificate", "last_school_report",
        ]

    # 🔎 Validation
    def validate(self, attrs):
        if attrs["password1"] != attrs["password2"]:
            raise serializers.ValidationError("Les mots de passe ne correspondent pas.")
        if User.objects.filter(username=attrs["username"]).exists():
            raise serializers.ValidationError("Ce nom d’utilisateur existe déjà. Veuillez en choisir un autre.")
        if User.objects.filter(email=attrs["email"]).exists():
            raise serializers.ValidationError("Cet email est déjà utilisé. Veuillez en choisir un autre.")
        return attrs

    def create(self, validated_data):
        # Extraire infos User
        username = validated_data.pop("username")
        email = validated_data.pop("email")
        password = validated_data.pop("password1")
        validated_data.pop("password2", None)
        first_name = validated_data.pop("first_name")
        last_name = validated_data.pop("last_name")
        sexe = validated_data.pop("sexe")

        # Créer User
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            sexe=sexe,          # ⬅️ propagé
            role="student",
            is_active=False,    # en attente validation admin
        )

        # Année académique active
        active_year = AcademicYear.objects.filter(is_active=True).first()
        if not active_year:
            raise serializers.ValidationError("Aucune année académique active.")

        # Créer Student
        student = Student.objects.create(
            user=user,
            academic_year=active_year,
            **validated_data
        )

        return student
