from rest_framework import serializers
from .models import Club, Event, Testimonial, GalleryItem

class ClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = "__all__"

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"

class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = "__all__"

class GalleryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = GalleryItem
        fields = "__all__"
