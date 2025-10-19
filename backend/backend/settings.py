"""
Django settings for backend project.

Clean, optimized, and ready for both local development and Render deployment.
"""

import os
from datetime import timedelta
from pathlib import Path
import environ

# ============================================================
# 📁 Base Directory
# ============================================================
BASE_DIR = Path(__file__).resolve().parent.parent

# ============================================================
# 🔑 Clés et configuration de base
# ============================================================
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

SECRET_KEY = env("SECRET_KEY", default="django-insecure-fallback-key")
DEBUG = env.bool("DEBUG", default=False)  # ⚠️ False pour Render

# ============================================================
# 🌍 Hôtes autorisés
# ============================================================
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]
if hostname := os.environ.get("RENDER_EXTERNAL_HOSTNAME"):
    ALLOWED_HOSTS.append(hostname)

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
if hostname:
    CSRF_TRUSTED_ORIGINS.append(f"https://{hostname}")

# ============================================================
# 🧩 Applications
# ============================================================
INSTALLED_APPS = [
    # Django core
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Apps locales
    "accounts",
    "academics",
    "core",
    "students",
    "alumni",
    "employees",
    "professors",
    "reports",
    "communication",
    "payments",
    "membersite",
    "blog",
    "programs.apps.ProgramsConfig",
    "schoollife",
    "about",
    "homepage",

    # Libs
    "rest_framework",
    "corsheaders",
    "drf_spectacular",
    "django_filters",
    "channels",
    "smart_selects",
]

# ============================================================
# ⚙️ Middlewares
# ============================================================
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # ✅ obligatoire Render
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
# 📡 URL et Templates
# ============================================================
ROOT_URLCONF = "backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "accounts" / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "communication.views.unread_count",
            ],
        },
    },
]

WSGI_APPLICATION = "backend.wsgi.application"
ASGI_APPLICATION = "backend.asgi.application"

# ============================================================
# 🧠 Channels (WebSocket + Redis)
# ============================================================
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}

# ============================================================
# 🗃️ Base de données
# ============================================================
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# ============================================================
# 🔐 Authentification
# ============================================================
AUTH_USER_MODEL = "accounts.User"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ============================================================
# 🌐 Internationalisation
# ============================================================
LANGUAGE_CODE = "fr"
LANGUAGES = [("fr", "Français"), ("en", "English")]
TIME_ZONE = "America/Port-au-Prince"
USE_I18N = True
USE_TZ = True

LOCALE_PATHS = [BASE_DIR / "locale"]

# ============================================================
# 📦 Fichiers statiques et médias
# ============================================================
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"  # ✅ pour Render
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ==============================
