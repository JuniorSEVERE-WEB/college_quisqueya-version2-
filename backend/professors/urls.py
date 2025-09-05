from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProfessorViewSet

router = DefaultRouter()
router.register(r"professors", ProfessorViewSet, basename="professor")

urlpatterns = [
    path("", include(router.urls)),
]
