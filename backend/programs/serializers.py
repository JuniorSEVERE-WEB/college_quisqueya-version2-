

from rest_framework import serializers
from .models import Program, Classroom

class ClassroomSerializer(serializers.ModelSerializer):
    program_label = serializers.CharField(source="program.get_name_display", read_only=True)

    class Meta:
        model = Classroom
        fields = ["id", "name", "program", "program_label", "created_at"]

class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = ["id", "name", "academic_year", "created_at"]
