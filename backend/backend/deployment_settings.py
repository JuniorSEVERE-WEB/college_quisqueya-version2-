import os
import dj_database_url
from .settings import *  # Importer toutes les configurations de base

# -----------------------------------------------------------
# 🔐 Sécurité et environnement Render
# -----------------------------------------------------------
DEBUG = False

SECRET_KEY = os.environ.get("SECRET_KEY", "fallback-secret-key")

# Détection automatique du domaine Render
RENDER_HOSTNAME = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
if RENDER_HOSTNAME:
    ALLOWED_HOSTS = [RENDER_HOSTNAME, "localhost", "127.0.0.1"]
    CSRF_TRUSTED_ORIGINS = [f"https://{RENDER_HOSTNAME}"]
else:
    ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# -----------------------------------------------------------
# 🧩 Middleware : Whitenoise pour les fichiers statiques
# -----------------------------------------------------------
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # Serve static files
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "core.middleware.CurrentUserMiddleware",
    "core.middleware.ActiveAcademicYearMiddleware",
]

# -----------------------------------------------------------
# 🗃️ Base de données PostgreSQL (Render)
# -----------------------------------------------------------
DATABASES = {
    "default": dj_database_url.config(
        default=os.environ.get("DATABASE_URL"),
        conn_max_age=600,  # pour garder la connexion active
    )
}

# -----------------------------------------------------------
# 🧾 Stockage statique (Whitenoise)
# -----------------------------------------------------------
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Répertoire pour collectstatic
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# -----------------------------------------------------------
# ✉️ Email (utilise tes variables Render)
# -----------------------------------------------------------
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# -----------------------------------------------------------
# 🌍 CORS (pour ton frontend Render)
# -----------------------------------------------------------
CORS_ALLOWED_ORIGINS = [
    "https://college-quisqueya-frontend.onrender.com",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

CSRF_TRUSTED_ORIGINS += [
    "https://college-quisqueya-frontend.onrender.com",
]

# -----------------------------------------------------------
# 📦 Stripe (faux en test)
# -----------------------------------------------------------
STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY", "test_secret_key")
STRIPE_PUBLISHABLE_KEY = os.environ.get("STRIPE_PUBLISHABLE_KEY", "test_publishable_key")
