# programs/api_views.py
from rest_framework import generics, permissions, serializers
from .models import Program, Classroom, Subject

# --- Serializers ---
class ProgramPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = ["id", "name"]

class ClassroomPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = ["id", "name"]

class SubjectPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ["id", "name"]

# --- Views ---
class ProgramPublicList(generics.ListAPIView):
    queryset = Program.objects.all().order_by("name")
    serializer_class = ProgramPublicSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

class ClassroomPublicList(generics.ListAPIView):
    queryset = Classroom.objects.all().order_by("name")
    serializer_class = ClassroomPublicSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

class SubjectPublicList(generics.ListAPIView):
    queryset = Subject.objects.all().order_by("name")
    serializer_class = SubjectPublicSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = []
