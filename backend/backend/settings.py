# Full settings.py for College Quisqueya (development-friendly)

import dj_database_url
import os
from datetime import timedelta
from pathlib import Path
import environ

# ============================================================
# 📁 Base Directory
# ============================================================
BASE_DIR = Path(__file__).resolve().parent.parent

# ============================================================
# 🔑 Environnement
# ============================================================
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

# ============================================================
# 🗃️ Database (Railway compliant)
# ============================================================
DATABASES = {
    'default': dj_database_url.config(
        conn_max_age=600,
        ssl_require=True
    )
}

SECRET_KEY = env("SECRET_KEY", default="django-insecure-fallback-key")
DEBUG = env.bool("DEBUG", default=True)

# ============================================================
# 🌍 Hôtes autorisés
# ============================================================
ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "juniorsevere.dev",           # Ton domaine
    ".railway.app",               # Autorise tous les sous-domaines Railway
    "collegequisqueya-version2-production.up.railway.app",  # Domaine de production spécifique
]
CSRF_TRUSTED_ORIGINS = [
    'https://collegequisqueya-version2-production.up.railway.app',
]

# add Render host if present
hostname = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
if hostname:
    ALLOWED_HOSTS.append(hostname)

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

    # Local apps
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

    # Third party
    "rest_framework",
    "corsheaders",
    "drf_spectacular",
    "django_filters",
    "channels",
    "smart_selects",
]

# ============================================================
# ⚙️ Middleware
# ============================================================
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # must be first for CORS
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
# 📡 URL / Templates
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
# 🧠 Channels
# ============================================================
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {"hosts": [("127.0.0.1", 6379)]},
    }
}

# ============================================================
# 🗃️ Database (dev: postgresql)
# ============================================================

# ============================================================
# 🔐 Authentication
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
# 📦 Static & Media
# ============================================================
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ============================================================
# ✉️ Email (dev safe)
# ============================================================
if DEBUG:
    # Print emails to console in development to avoid SMTP errors
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
    DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default="no-reply@college-quisqueya.local")
else:
    EMAIL_BACKEND = env("EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend")
    EMAIL_HOST = env("EMAIL_HOST", default="smtp.gmail.com")
    EMAIL_PORT = env.int("EMAIL_PORT", default=587)
    EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS", default=True)
    EMAIL_HOST_USER = env("EMAIL_HOST_USER", default="")
    EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default="")
    DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default=EMAIL_HOST_USER)

# ============================================================
# 💳 Stripe keys (optional)
# ============================================================
STRIPE_SECRET_KEY = env("STRIPE_SECRET_KEY", default="")
STRIPE_PUBLISHABLE_KEY = env("STRIPE_PUBLISHABLE_KEY", default="")

# ============================================================
# 🧾 DRF
# ============================================================
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.AllowAny"],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 6,
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.OrderingFilter",
        "rest_framework.filters.SearchFilter",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

# ============================================================
# 🔐 JWT
# ============================================================
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=3),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=14),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "AUTH_HEADER_TYPES": ("Bearer",),
}

# ============================================================
# 🧩 Misc
# ============================================================
CORE_ACADEMIC_YEAR_MODEL = "students.AcademicYear"
SMART_SELECTS_JQUERY = True

# ============================================================
# 🌍 CORS & CSRF configuration (dev-first)
# ============================================================
# Allowed origins for frontend (used when CORS_ALLOW_ALL_ORIGINS is False)
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://college-quisqueya-version2-17.onrender.com",
]

CORS_ALLOW_CREDENTIALS = True

# CSRF trusted origins (include ports and schemes)
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://college-quisqueya-version2-16.onrender.com",
    "https://college-quisqueya-version2-17.onrender.com",
]

# Dev cookie/CSRF settings (unsafe for production)
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_SAMESITE = "Lax"

# Toggle behavior based on DEBUG
if DEBUG:
    # simpler local dev: allow all origins
    CORS_ALLOW_ALL_ORIGINS = True
    ALLOWED_HOSTS.extend(["localhost", "127.0.0.1", "0.0.0.0"])
else:
    CORS_ALLOW_ALL_ORIGINS = False
    # In production, ensure CSRF_COOKIE_SECURE = True and SESSION_COOKIE_SECURE = True

# ============================================================
# 🧾 Logging minimal (console)
# ============================================================
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": "INFO"},
}

# End of settings.py
# Make sure to:
# - install requirements: pip install -r requirements.txt
# - create a .env with SECRET_KEY and other production vars
# - restart the dev server after changes