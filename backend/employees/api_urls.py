# employees/api_urls.py
from django.urls import path
from .api_views import EmployeeRegisterView

urlpatterns = [
    path("register/", EmployeeRegisterView.as_view(), name="employee_register"),
]
