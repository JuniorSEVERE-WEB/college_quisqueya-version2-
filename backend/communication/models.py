from django.db import models
from django.contrib.auth import get_user_model
from academics.models import Classroom  # supposons que tu as un modèle Classroom

User = get_user_model()


# 💬 Messagerie interne entre utilisateurs (professeurs, élèves, admins, etc.)
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    recipients = models.ManyToManyField(User, related_name="received_messages")
    subject = models.CharField(max_length=255)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read_by = models.ManyToManyField(User, related_name="read_messages", blank=True)

    def __str__(self):
        return f"{self.subject} (de {self.sender})"


# 📩 Formulaire de contact public (visiteurs → administration)
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.subject}"
