# accounts/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.db import transaction
from .utils import send_activation_email

User = get_user_model()

@receiver(post_save, sender=User)
def send_email_when_user_activated(sender, instance, created, **kwargs):
    """
    Envoie un email automatiquement quand un utilisateur passe de inactif à actif.
    """
    if not created:  # On ne gère que la modification
        # On récupère l’état précédent depuis la base
        try:
            old_instance = User.objects.get(pk=instance.pk)
        except User.DoesNotExist:
            old_instance = None

        if old_instance and not old_instance.is_active and instance.is_active:
            # L’utilisateur vient d’être activé
            # on attend la fin de la transaction pour éviter les envois multiples
            transaction.on_commit(lambda: send_activation_email(instance))
