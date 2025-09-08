# accounts/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .utils import send_activation_email

User = get_user_model()

@receiver(post_save, sender=User)
def send_email_when_user_activated(sender, instance, created, **kwargs):
    """
    Envoie un email automatiquement quand un utilisateur passe de inactif à actif.
    """
    if not created:  # On ignore la création, on regarde uniquement les mises à jour
        # Vérifie si l'utilisateur vient d'être activé
        if instance.is_active:
            print(f"📩 Signal déclenché pour {instance.username} (email: {instance.email})")
            send_activation_email(instance)
