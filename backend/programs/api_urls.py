from django.urls import path
from .api_views import ClassroomPublicList

urlpatterns = [
  path("classrooms/public/", ClassroomPublicList.as_view(), name="classrooms-public"),
]