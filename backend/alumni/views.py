from rest_framework import viewsets, permissions
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from .models import Alumni
from .serializers import AlumniSerializer

class AlumniViewSet(viewsets.ModelViewSet):
    queryset = Alumni.objects.select_related("user").all().order_by("-date_created")
    serializer_class = AlumniSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser, FormParser, JSONParser]


    filterset_fields = ["role", "year_left", "user"]
    search_fields = ["promo_name", "user__email"]
    ordering_fields = ["date_created", "id"]

    def get_queryset(self):
        qs = super().get_queryset()
        # Filtres: ?role=student&year_left=2024&user=<id>&q=<search>
        role = self.request.query_params.get("role")
        year_left = self.request.query_params.get("year_left")
        user_id = self.request.query_params.get("user")
        q = self.request.query_params.get("q")

        if role:
            qs = qs.filter(role=role)
        if year_left:
            qs = qs.filter(year_left=year_left)
        if user_id:
            qs = qs.filter(user_id=user_id)
        if q:
            qs = qs.filter(promo_name__icontains=q)
        return qs

    def perform_create(self, serializer):
        # Si aucun user n’est envoyé, on met l’utilisateur courant
        user = serializer.validated_data.get("user") or self.request.user if self.request.user.is_authenticated else None
        serializer.save(user=user)




