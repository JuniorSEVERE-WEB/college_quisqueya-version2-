"""
ASGI config for backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

This configuration supports both:
- Standard HTTP requests (Django)
- WebSocket connections (via Django Channels)
"""

import os
from django.core.asgi import get_asgi_application

# 🔧 Choix du fichier de configuration Django
# Pour Render → on utilise backend.deployment_settings
# Pour le local → backend.settings
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    os.environ.get("DJANGO_SETTINGS_MODULE", "backend.deployment_settings")
)

# Import de Channels
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

# ⚠️ Si tu n’as pas encore de routes WebSocket, on peut laisser vide pour l’instant
# Plus tard, tu pourras importer tes routes :
# from core import routing as core_routing
# websocket_urlpatterns = core_routing.websocket_urlpatterns

# Application principale ASGI
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    # "websocket": AuthMiddlewareStack(
    #     URLRouter(websocket_urlpatterns)
    # ),
})
