from django.urls import path
from .api_views import ClubListView, ClubDetailView, EventListView, EventDetailView

urlpatterns = [
    # Clubs
    path("clubs/", ClubListView.as_view(), name="clubs-list"),
    path("clubs/<int:pk>/", ClubDetailView.as_view(), name="clubs-detail"),

    # Events
    path("events/", EventListView.as_view(), name="events-list"),
    path("events/<int:pk>/", EventDetailView.as_view(), name="events-detail"),
]
