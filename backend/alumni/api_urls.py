# alumni/api_urls.py
from rest_framework.routers import DefaultRouter
from .views import AlumniViewSet

router = DefaultRouter()
router.register(r"", AlumniViewSet, basename="alumni")

urlpatterns = router.urls
