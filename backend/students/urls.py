from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet, StudentRegisterView

router = DefaultRouter()
router.register(r"students", StudentViewSet, basename="student")

urlpatterns = [
    path("students/register/", StudentRegisterView.as_view(), name="student-register"),
    path("", include(router.urls)),
]
