# programs/api_urls.py
from django.urls import path
from .api_views import ProgramPublicList, ClassroomPublicList, SubjectPublicList

urlpatterns = [
    path("programs/public/", ProgramPublicList.as_view(), name="programs-public"),
    path("classrooms/public/", ClassroomPublicList.as_view(), name="classrooms-public"),
    path("subjects/public/", SubjectPublicList.as_view(), name="subjects-public"),
]
