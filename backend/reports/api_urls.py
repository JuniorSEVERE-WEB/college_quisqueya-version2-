from rest_framework.routers import DefaultRouter
from .api_views import ReportSessionViewSet, SubjectCoefficientViewSet, GradeViewSet

router = DefaultRouter()
router.register("report-sessions", ReportSessionViewSet, basename="reportsession")
router.register("subject-coefficients", SubjectCoefficientViewSet, basename="subjectcoefficient")
router.register("grades", GradeViewSet, basename="grade")

urlpatterns = router.urls