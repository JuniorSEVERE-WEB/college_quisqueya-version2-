from django.urls import path
from .api_views import (
    SlideListView,
    WelcomeListView,
    ValueListView,
    SiteSettingsView,
)

urlpatterns = [
    path("slides/", SlideListView.as_view(), name="slide-list"),
    path("welcome/", WelcomeListView.as_view(), name="welcome-list"),
    path("values/", ValueListView.as_view(), name="value-list"),
    path("settings/", SiteSettingsView.as_view(), name="site-settings"),
]
