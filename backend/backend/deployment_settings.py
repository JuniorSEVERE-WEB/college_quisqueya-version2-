import os
import dj_database_url
from .settings import *  # Importer les paramètres de base

# ============================================================
# 🔐 Sécurité & Debug
# ============================================================
DEBUG = False
SECRET_KEY = os.environ.get("SECRET_KEY", "fallback-secret-key")

# ============================================================
# 🌍 Hôtes et CSRF
# ============================================================
RENDER_HOSTNAME = os.environ.get("RENDER_EXTERNAL_HOSTNAME")

ALLOWED_HOSTS = [
    "api.collegequisqueyadeleogane.juniorsevere.dev",
    "collegequisqueyadeleogane.juniorsevere.dev",
    "localhost",
    "127.0.0.1",
]
if RENDER_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_HOSTNAME)

CSRF_TRUSTED_ORIGINS = [
    "https://api.collegequisqueyadeleogane.juniorsevere.dev",
    "https://collegequisqueyadeleogane.juniorsevere.dev",
]
if RENDER_HOSTNAME:
    CSRF_TRUSTED_ORIGINS.append(f"https://{RENDER_HOSTNAME}")

# ============================================================
# 🧱 Middleware (avec Whitenoise pour les fichiers statiques)
# ============================================================
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
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

# ============================================================
# 🗄️ Base de données (Render + local)
# ============================================================
DATABASES = {
    "default": dj_database_url.config(
        default=os.environ.get("DATABASE_URL"),
        conn_max_age=600,
    )
}

# ============================================================
# 📦 Fichiers statiques & médias   nnnnnnnnnnn
# ============================================================
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
}

# ============================================================
# ✉️ Email (optionnel pour activation compte)
# ============================================================
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# ============================================================
# 🌐 CORS et CSRF (frontend autorisé)
# ============================================================
CORS_ALLOWED_ORIGINS = [
    "https://collegequisqueyadeleogane.juniorsevere.dev",
    "https://api.collegequisqueyadeleogane.juniorsevere.dev",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

CSRF_TRUSTED_ORIGINS += [
    "https://collegequisqueyadeleogane.juniorsevere.dev",
]

# ============================================================
# 💳 Stripe (si paiement activé)
# ============================================================
STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY", "test_secret_key")
STRIPE_PUBLISHABLE_KEY = os.environ.get("STRIPE_PUBLISHABLE_KEY", "test_publishable_key")

# ============================================================
# 🧾 Logging (afficher dans les logs Render)
# ============================================================
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": "INFO"},
}
