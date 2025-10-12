# backend/academics/api_views.py
from rest_framework import generics, permissions, serializers
from programs.models import Classroom  # ✅ Import corrigé ici
from programs.serializers import ClassroomSerializer  # ✅ si tu as déjà un serializer dans programs
# sinon tu peux garder ton ClassroomSerializer local

# ✅ Serializer public simplifié
class ClassroomPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = ["id", "name"]

# ✅ Endpoint public qui retourne toutes les classes existantes
class ActiveClassroomsPublicList(generics.ListAPIView):
    queryset = Classroom.objects.all().order_by("name")
    serializer_class = ClassroomPublicSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = []
    pagination_class = None
