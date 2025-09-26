from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProgramViewSet, ClassroomViewSet, SubjectViewSet

router = DefaultRouter()
router.register(r"programs", ProgramViewSet)
router.register(r"classrooms", ClassroomViewSet, basename="classroom")
router.register(r"subjects", SubjectViewSet, basename="subject")

urlpatterns = [
    path("", include(router.urls)),
]
