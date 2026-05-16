# L'envoi d'email pour les messages de contact est centralisé
# dans ContactMessageViewSet.perform_create (views_api.py) avec fail_silently=True,
# afin qu'un échec SMTP ne casse pas la création du message côté API.
