from django.urls import path
from .api_views import AboutPageView

urlpatterns = [
    path("about/", AboutPageView.as_view(), name="about-page"),
]
