from django.core.mail import send_mail
from django.conf import settings

def send_activation_email(user):
    subject = "Votre compte a été validé ✅"
    message = f"""
Bonjour {user.username},

Votre compte sur le site de l’école a été validé par l’administration.
Vous pouvez maintenant vous connecter et accéder à vos informations.

Cordialement,
L’administration scolaire.
"""
    send_mail(
        subject,
        message,
        "no-reply@college-quisqueya.ht", 
        [user.email],
        fail_silently=False,
    )
