from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Alumni

User = get_user_model()


class AlumniRegisterSerializer(serializers.ModelSerializer):
    """
    Serializer pour l'inscription des anciens élèves (Alumni).
    Crée d'abord un utilisateur, puis un objet Alumni lié.
    """
    # 🔹 Champs User
    username = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    phone = serializers.CharField(required=True, write_only=True)
    sexe = serializers.ChoiceField(choices=User.SEXE_CHOICES, required=True, write_only=True)

    class Meta:
        model = Alumni
        fields = [
            # Champs User
            "username", "email", "password1", "password2",
            "first_name", "last_name", "sexe", "phone",
            # Champs Alumni
            "year_left", "promo_name", "years_interval", "proof_document",
        ]

    # ✅ Validation des champs avant création
    def validate(self, attrs):
        if attrs["password1"] != attrs["password2"]:
            raise serializers.ValidationError("Les mots de passe ne correspondent pas.")
        if User.objects.filter(username=attrs["username"]).exists():
            raise serializers.ValidationError("Ce nom d’utilisateur existe déjà.")
        if User.objects.filter(email=attrs["email"]).exists():
            raise serializers.ValidationError("Cet email est déjà utilisé.")
        return attrs

    # ✅ Création du compte User + Alumni
    def create(self, validated_data):
        # Extraire les champs User
        username = validated_data.pop("username")
        email = validated_data.pop("email")
        password = validated_data.pop("password1")
        validated_data.pop("password2", None)
        first_name = validated_data.pop("first_name")
        last_name = validated_data.pop("last_name")
        phone = validated_data.pop("phone")
        sexe = validated_data.pop("sexe")

        # 🔹 Création de l'utilisateur
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            sexe=sexe,
            role="alumni_student",  # cohérent avec ton modèle User
            is_active=False,        # en attente de validation par l’administration
        )

        # 🔹 Création de l’Alumni lié à l’utilisateur
        alumni = Alumni.objects.create(
            user=user,
            **validated_data
        )

        return alumni
