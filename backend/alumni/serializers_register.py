# alumni/serializers_register.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Alumni

User = get_user_model()

class AlumniRegisterSerializer(serializers.ModelSerializer):
    # Champs User
    username = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)

    class Meta:
        model = Alumni
        fields = [
            "username", "email", "password1", "password2",
            "first_name", "last_name",
            "year_left", "promo_name", "years_interval",
            "proof_document",
        ]

    def validate(self, attrs):
        if attrs["password1"] != attrs["password2"]:
            raise serializers.ValidationError("Les mots de passe ne correspondent pas.")
        if User.objects.filter(username=attrs["username"]).exists():
            raise serializers.ValidationError("Ce nom d’utilisateur existe déjà. Veuillez en choisir un autre.")
        if User.objects.filter(email=attrs["email"]).exists():
            raise serializers.ValidationError("Cet email est déjà utilisé. Veuillez en choisir un autre.")
        return attrs

    def create(self, validated_data):
        username = validated_data.pop("username")
        email = validated_data.pop("email")
        password = validated_data.pop("password1")
        validated_data.pop("password2", None)
        first_name = validated_data.pop("first_name")
        last_name = validated_data.pop("last_name")

        # Créer User
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            role="alumni",
            is_active=False,  # en attente validation admin
        )

        # Créer Alumni
        alumni = Alumni.objects.create(
            user=user,
            **validated_data
        )
        return alumni
