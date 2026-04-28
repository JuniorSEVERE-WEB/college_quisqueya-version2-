from django.urls import path
from .api_views import (
    EmailOrUsernameTokenObtainPairView,
    MeView,
    AbonneRegisterView,
    GoogleAuthView,
)
from rest_framework_simplejwt.views import TokenRefreshView
from . import api_views_password_reset

urlpatterns = [
    # Auth JWT
    path("token/", EmailOrUsernameTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # Profil courant
    path("me/", MeView.as_view(), name="me"),

    # Inscription abonné(e)
    path("register/abonne/", AbonneRegisterView.as_view(), name="register_abonne"),

    # OAuth Google
    path("google/", GoogleAuthView.as_view(), name="google_auth"),

    # Réinitialisation de mot de passe
    path("password-reset/", api_views_password_reset.PasswordResetAPIView.as_view(), name="api_password_reset"),
    path("password-reset-confirm/", api_views_password_reset.PasswordResetConfirmAPIView.as_view(), name="api_password_reset_confirm"),
]
