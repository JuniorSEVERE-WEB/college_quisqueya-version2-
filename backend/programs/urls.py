from rest_framework.routers import DefaultRouter
from .views import ProgramViewSet, ClassroomViewSet

router = DefaultRouter()
router.register(r"programs", ProgramViewSet)
router.register(r"classrooms", ClassroomViewSet, basename="classroom")

urlpatterns = router.urls
