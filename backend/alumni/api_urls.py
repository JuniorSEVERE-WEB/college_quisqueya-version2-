# alumni/api_urls.py
from django.urls import path
from .views_register import AlumniRegisterAPIView
from rest_framework.routers import DefaultRouter
from .views import AlumniViewSet

router = DefaultRouter()
router.register(r"", AlumniViewSet, basename="alumni")

urlpatterns = [
    path("register/", AlumniRegisterAPIView.as_view(), name="alumni-register"),
]

urlpatterns += router.urls
