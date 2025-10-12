import os 
import dj_database_url 
from .settings import *  # Importer toutes les configurations de base
from .settings import BASE_DIR  

ALLOWED_HOSTS = [os.environ.get('RENDER_EXTERNAL_HOSTNAME')]
CSRF_TRUSTED_ORIGINS = ['https://'+os.environ.get('RENDER_EXTERNAL_HOSTNAME')]

DEBGUG = False 
SECRET_KEY = os.environ.get['SECRET_KEY']

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # <-- remplace "corsheaders"
    'django.middleware.security.SecurityMiddleware',

    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'core.middleware.CurrentUserMiddleware',
    'core.middleware.ActiveAcademicYearMiddleware',
    # supprime "drf_spectacular" ici (ce n’est pas un middleware)
]

"""
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

"""

STORAGES = {
    'default':{
        'BACKEND' : "django.core.files.storage.FileSystemStorage",
    },
    'staticfiles': {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}

DATABASES = {
    "default": dj_database_url.config(
        default = os.environ['DATABASE_URL'],
        conn_max_age=600
    )
}






