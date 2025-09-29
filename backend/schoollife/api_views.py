from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import Club, Event, Testimonial, GalleryItem
from .serializers import (
    ClubSerializer, EventSerializer,
    TestimonialSerializer, GalleryItemSerializer
)

# Clubs
class ClubListView(generics.ListAPIView):
    queryset = Club.objects.all().order_by("id")
    serializer_class = ClubSerializer
    permission_classes = [AllowAny]

class ClubDetailView(generics.RetrieveAPIView):
    queryset = Club.objects.all()
    serializer_class = ClubSerializer
    permission_classes = [AllowAny]


# Events
class EventListView(generics.ListAPIView):
    queryset = Event.objects.all().order_by("-date")
    serializer_class = EventSerializer
    permission_classes = [AllowAny]

class EventDetailView(generics.RetrieveAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [AllowAny]


# Testimonials
class TestimonialListView(generics.ListAPIView):
    queryset = Testimonial.objects.all().order_by("-id")
    serializer_class = TestimonialSerializer
    permission_classes = [AllowAny]

class TestimonialDetailView(generics.RetrieveAPIView):
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer
    permission_classes = [AllowAny]


# Gallery
class GalleryListView(generics.ListAPIView):
    queryset = GalleryItem.objects.all().order_by("-date_added")
    serializer_class = GalleryItemSerializer
    permission_classes = [AllowAny]

class GalleryDetailView(generics.RetrieveAPIView):
    queryset = GalleryItem.objects.all()
    serializer_class = GalleryItemSerializer
    permission_classes = [AllowAny]
