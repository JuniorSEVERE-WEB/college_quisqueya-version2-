from django.urls import path
from .api_views import EmailOrUsernameTokenObtainPairView, MeView

urlpatterns = [
    path("token/", EmailOrUsernameTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("me/", MeView.as_view(), name="me"),
]