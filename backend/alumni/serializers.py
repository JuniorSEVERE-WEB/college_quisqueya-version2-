from rest_framework import serializers
from .models import Alumni
from accounts.models import User

class AlumniSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    user_full_name = serializers.CharField(source="user.get_full_name", read_only=True)
    user_email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = Alumni
        fields = [
            "id",
            "user", "user_full_name", "user_email",
            "role", "year_left", "promo_name", "years_interval",
            "proof_document",
            "date_created",
        ]
        read_only_fields = ["date_created"]