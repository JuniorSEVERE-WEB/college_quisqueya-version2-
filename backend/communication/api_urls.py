from rest_framework.routers import DefaultRouter
from .views_api import MessageViewSet, ContactMessageViewSet

router = DefaultRouter()
router.register(r"messages", MessageViewSet, basename="message")
router.register(r"contact-messages", ContactMessageViewSet, basename="contact-message")

urlpatterns = router.urls
