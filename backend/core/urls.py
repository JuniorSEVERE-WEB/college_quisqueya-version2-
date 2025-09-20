from django.urls import path
from .views import core_debug

urlpatterns = [
    path("debug/", core_debug, name="core_debug"),
]