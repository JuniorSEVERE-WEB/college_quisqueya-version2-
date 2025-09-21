from rest_framework import serializers
from .models import Message
from accounts.models import User  # ou get_user_model()

class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source="sender.username", read_only=True)
    recipients = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)
    recipients_usernames = serializers.SlugRelatedField(
        slug_field="username", read_only=True, many=True, source="recipients"
    )
    read_by_usernames = serializers.SlugRelatedField(
        slug_field="username", read_only=True, many=True, source="read_by"
    )

    class Meta:
        model = Message
        fields = [
            "id",
            "sender", "sender_username",
            "recipients", "recipients_usernames",
            "subject", "body",
            "created_at",
            "read_by", "read_by_usernames",
        ]
        read_only_fields = ["sender", "created_at", "read_by"]
