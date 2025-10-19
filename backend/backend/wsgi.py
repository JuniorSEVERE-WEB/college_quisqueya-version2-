"""
WSGI config for backend project.
It exposes the WSGI callable as a module-level variable named ``application``.
"""

import os
from django.core.wsgi import get_wsgi_application

# ✅ Utiliser le bon fichier de settings pour Render
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.deployment_settings")

application = get_wsgi_application()
