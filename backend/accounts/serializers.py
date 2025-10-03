from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id", "username", "email", "first_name", "last_name",
            "role", "sexe", "photo"
        )


class AbonneRegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    sexe = serializers.ChoiceField(choices=User.SEXE_CHOICES, required=True)
    phone = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "sexe", "phone"]

    def validate(self, data):
        if data["password1"] != data["password2"]:
            raise serializers.ValidationError("Les mots de passe ne correspondent pas.")
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password1"],
            role="abonne",
            sexe=validated_data["sexe"],
            phone=validated_data["phone"]
        )
        return user

