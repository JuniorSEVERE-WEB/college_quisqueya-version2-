from django.urls import path
from .api_views import (
    EmailOrUsernameTokenObtainPairView,
    MeView,
    AbonneRegisterView,
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
     path("password-reset/", api_views_password_reset.PasswordResetAPIView.as_view(), name="password_reset"),
]
