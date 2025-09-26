from rest_framework import generics, permissions, serializers
from .models import Classroom

class ClassroomPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = ["id", "name"]  # champs sûrs

class ActiveClassroomsPublicList(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ClassroomPublicSerializer
    pagination_class = None

    def get_queryset(self):
        # Si vous avez un flag is_active ou une année académique active, adaptez ici.
        return Classroom.objects.all().order_by("name")