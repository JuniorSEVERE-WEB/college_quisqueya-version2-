from rest_framework import serializers
from .models import Slide, SlideTitle, Welcome, Value


class SlideTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SlideTitle
        fields = ["id", "title"]


class SlideSerializer(serializers.ModelSerializer):
    titles = SlideTitleSerializer(many=True, read_only=True)

    class Meta:
        model = Slide
        fields = ["id", "image", "text", "titles"]


class WelcomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Welcome
        fields = "__all__"


class ValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Value
        fields = "__all__"
