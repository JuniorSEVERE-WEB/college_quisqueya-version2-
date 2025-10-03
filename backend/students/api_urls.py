# students/api_urls.py
from django.urls import path
from .api_views import StudentRegisterView

urlpatterns = [
    path("register/", StudentRegisterView.as_view(), name="student_register"),
]
