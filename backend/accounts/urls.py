from django.urls import path
from . import views

urlpatterns = [
    path("register/student/", views.register, name="register_student"),  # tu peux garder comme ça
]
