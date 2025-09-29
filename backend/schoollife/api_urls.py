from django.urls import path
from .api_views import (
    ClubListView, ClubDetailView,
    EventListView, EventDetailView,
    TestimonialListView, TestimonialDetailView,
    GalleryListView, GalleryDetailView
)

urlpatterns = [
    # Clubs
    path("clubs/", ClubListView.as_view(), name="club-list"),
    path("clubs/<int:pk>/", ClubDetailView.as_view(), name="club-detail"),

    # Events
    path("events/", EventListView.as_view(), name="event-list"),
    path("events/<int:pk>/", EventDetailView.as_view(), name="event-detail"),

    # Testimonials
    path("testimonials/", TestimonialListView.as_view(), name="testimonial-list"),
    path("testimonials/<int:pk>/", TestimonialDetailView.as_view(), name="testimonial-detail"),

    # Gallery
    path("gallery/", GalleryListView.as_view(), name="gallery-list"),
    path("gallery/<int:pk>/", GalleryDetailView.as_view(), name="gallery-detail"),
]
