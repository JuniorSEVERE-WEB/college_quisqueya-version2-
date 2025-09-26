from django.urls import path
from .api_views import ActiveClassroomsPublicList

urlpatterns = [
    path("classrooms/active/", ActiveClassroomsPublicList.as_view(), name="academics-classrooms-active"),
]