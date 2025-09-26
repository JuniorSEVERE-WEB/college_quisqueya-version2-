from rest_framework import generics, permissions, serializers
from .models import Classroom

class ClassroomPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = ["id", "name"]

class ClassroomPublicList(generics.ListAPIView):
    queryset = Classroom.objects.all().order_by("name")
    serializer_class = ClassroomPublicSerializer
    permission_classes = [permissions.AllowAny]  # <- public
    authentication_classes = []  # <- désactive JWT obligatoire
