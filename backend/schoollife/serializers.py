from rest_framework import serializers
from .models import Club, Event


class ClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = "__all__"   # id, name, description, image


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"   # id, title, description, date, image
