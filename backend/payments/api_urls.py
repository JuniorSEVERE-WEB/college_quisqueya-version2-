from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DonationViewSet, EnrollmentFeeViewSet

router = DefaultRouter()
router.register(r"donations", DonationViewSet, basename="donation")
router.register(r"enrollment-fees", EnrollmentFeeViewSet, basename="enrollmentfee")

urlpatterns = [
    path("", include(router.urls)),
]
