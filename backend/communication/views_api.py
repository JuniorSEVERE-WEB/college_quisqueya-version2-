from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from .models import Message, ContactMessage
from .serializers import MessageSerializer, ContactMessageSerializer


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


class ContactMessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour créer des messages de contact.

    Par défaut, toute personne (authenticated ou anonyme) peut créer un message.
    Seuls les utilisateurs staff ou superusers peuvent lister et consulter les messages.
    """

    queryset = ContactMessage.objects.all().order_by("-created_at")
    serializer_class = ContactMessageSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve", "update", "partial_update", "destroy"]:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        contact = serializer.save()
        from_email = settings.DEFAULT_FROM_EMAIL

        recipient = getattr(settings, "CONTACT_RECIPIENT_EMAIL", "")
        if recipient:
            send_mail(
                subject=f"[Contact] {contact.subject}",
                message=(
                    f"Nom : {contact.name}\n"
                    f"Email : {contact.email}\n"
                    f"Sujet : {contact.subject}\n\n"
                    f"{contact.message}"
                ),
                from_email=from_email,
                recipient_list=[recipient],
                fail_silently=True,
            )

        if contact.email:
            send_mail(
                subject="Merci de nous avoir contactés - Collège Quisqueya",
                message=(
                    f"Bonjour {contact.name},\n\n"
                    f"Nous avons bien reçu votre message concernant : \"{contact.subject}\".\n"
                    f"Notre équipe vous répondra dans les plus brefs délais.\n\n"
                    f"Copie de votre message :\n{contact.message}\n\n"
                    f"Merci de votre confiance,\n"
                    f"L'équipe du Collège Quisqueya"
                ),
                from_email=from_email,
                recipient_list=[contact.email],
                fail_silently=True,
            )
