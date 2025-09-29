from rest_framework import serializers
from .models import (
    AboutInfo, TimelineEvent, Founder, StaffMember,
    Value, KeyStat, Vision, ExamResult
)

class AboutInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutInfo
        fields = "__all__"

class TimelineEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimelineEvent
        fields = "__all__"

class FounderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Founder
        fields = "__all__"

class StaffMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffMember
        fields = "__all__"

class ValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Value
        fields = "__all__"

class KeyStatSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyStat
        fields = "__all__"

class VisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vision
        fields = "__all__"

class ExamResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamResult
        fields = "__all__"
