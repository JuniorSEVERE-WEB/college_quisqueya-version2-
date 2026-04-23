# accounts/signals.py
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .utils import send_activation_email
import logging

logger = logging.getLogger(__name__)
User = get_user_model()

@receiver(pre_save, sender=User)
def cache_previous_active_state(sender, instance, **kwargs):
    """Mémorise l'état is_active avant la sauvegarde."""
    if instance.pk:
        try:
            instance._was_active = User.objects.filter(pk=instance.pk).values_list('is_active', flat=True).first()
        except Exception:
            instance._was_active = None
    else:
        instance._was_active = None

@receiver(post_save, sender=User)
def send_email_when_user_activated(sender, instance, created, **kwargs):
    """Envoie un email uniquement quand un compte passe de inactif → actif."""
    if created:
        return
    was_active = getattr(instance, '_was_active', None)
    if was_active is False and instance.is_active:
        print(f"📩 Signal déclenché pour {instance.username} (email: {instance.email})")
        try:
            send_activation_email(instance)
        except Exception as e:
            logger.error(f"Échec envoi email activation pour {instance.email}: {e}")
