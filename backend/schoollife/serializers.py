from rest_framework import serializers
from .models import Club, Event, Testimonial, GalleryItem


class ClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = ["id", "name", "description", "photo"]  # ✅ ajout photo


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ["id", "club", "title", "description", "date", "logo"]  # ✅ ajout logo


class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = ["id", "name", "role", "message", "photo"]


class GalleryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = GalleryItem
        fields = ["id", "title", "image", "date_added"]
