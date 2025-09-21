from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Message
from .serializers import MessageSerializer

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        box = self.request.query_params.get("box")

        # ?box=inbox ou ?box=sent
        if box == "sent":
            return Message.objects.filter(sender=user).order_by("-created_at")
        return Message.objects.filter(recipients=user).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

    @action(detail=True, methods=["post"])
    def mark_as_read(self, request, pk=None):
        """Marquer un message comme lu"""
        msg = self.get_object()
        if request.user in msg.recipients.all() and request.user not in msg.read_by.all():
            msg.read_by.add(request.user)
        return Response({"status": "marked as read"})
