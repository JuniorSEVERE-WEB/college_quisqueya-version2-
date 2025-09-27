from django.urls import path
from .api_views import (
    EmailOrUsernameTokenObtainPairView,
    MeView,
    AbonneRegisterView,
)

urlpatterns = [
    path("token/", EmailOrUsernameTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("me/", MeView.as_view(), name="me"),
    path("register/abonne/", AbonneRegisterView.as_view(), name="register-abonne"),
]
