from rest_framework import routers
from .views import (
    AcademicYearViewSet, TrimesterViewSet, StepViewSet, ClassroomViewSet, SubjectViewSet,
    ProfessorViewSet, StudentViewSet, NoteViewSet, ResourceViewSet, AssignmentViewSet, SubmissionViewSet
)

router = routers.DefaultRouter()
router.register(r'academic-years', AcademicYearViewSet)
router.register(r'trimesters', TrimesterViewSet)
router.register(r'steps', StepViewSet)
router.register(r'classrooms', ClassroomViewSet)
router.register(r'subjects', SubjectViewSet)
router.register(r'professors', ProfessorViewSet)
router.register(r'students', StudentViewSet)
router.register(r'notes', NoteViewSet)
router.register(r'resources', ResourceViewSet)
router.register(r'assignments', AssignmentViewSet)
router.register(r'submissions', SubmissionViewSet)

urlpatterns = router.urls