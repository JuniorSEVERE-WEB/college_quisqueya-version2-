# programs/serializers.py
from rest_framework import serializers
from .models import Program, Classroom, Subject


class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = ["id", "name"]


class ClassroomSerializer(serializers.ModelSerializer):
    # Champ calculé automatiquement
    program_name = serializers.CharField(source="program.get_name_display", read_only=True)

    class Meta:
        model = Classroom
        fields = ["id", "name", "program", "program_name"]


class SubjectSerializer(serializers.ModelSerializer):
    classroom_name = serializers.CharField(source="classroom.name", read_only=True)
    program_name = serializers.CharField(source="classroom.program.get_name_display", read_only=True)

    class Meta:
        model = Subject
        fields = ["id", "name", "classroom", "classroom_name", "program_name"]
