from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import ContactMessage
from django.conf import settings


@receiver(post_save, sender=ContactMessage)
def send_contact_email(sender, instance, created, **kwargs):
    if created:
        # 📩 Email au staff/admin
        subject_admin = f"Nouveau message de contact : {instance.subject}"
        message_admin = (
            f"Vous avez reçu un nouveau message via le site Collège Quisqueya :\n\n"
            f"Nom : {instance.name}\n"
            f"Email : {instance.email}\n\n"
            f"Message :\n{instance.message}\n\n"
            f"Date : {instance.created_at}"
        )
        send_mail(
            subject_admin,
            message_admin,
            settings.DEFAULT_FROM_EMAIL,
            ["admin@collegequisqueya.ht"],  # 👉 change par ton email staff
            fail_silently=False,
        )

        # 📩 Accusé de réception au visiteur
        subject_user = "Merci de nous avoir contactés - Collège Quisqueya"
        message_user = (
            f"Bonjour {instance.name},\n\n"
            f"Nous avons bien reçu votre message concernant : \"{instance.subject}\".\n"
            f"Notre équipe vous répondra dans les plus brefs délais.\n\n"
            f"Copie de votre message :\n{instance.message}\n\n"
            f"Merci de votre confiance,\n"
            f"L’équipe du Collège Quisqueya"
        )
        send_mail(
            subject_user,
            message_user,
            settings.DEFAULT_FROM_EMAIL,
            [instance.email],  # 👈 l’adresse du visiteur
            fail_silently=False,
        )
