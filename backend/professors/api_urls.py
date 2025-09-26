# professors/api_urls.py
from django.urls import path
from .api_views import ProfessorRegisterView

urlpatterns = [
    path("register/", ProfessorRegisterView.as_view(), name="professor-register"),
]
