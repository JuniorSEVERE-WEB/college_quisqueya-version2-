from rest_framework import generics
from core.permissions import IsAbonneOrStudentOrProf
from .models import Club, Event, Testimonial, GalleryItem
from .serializers import (
    ClubSerializer, EventSerializer,
    TestimonialSerializer, GalleryItemSerializer
)

# Clubs
class ClubListView(generics.ListAPIView):
    queryset = Club.objects.all().order_by("id")
    serializer_class = ClubSerializer
    permission_classes = [IsAbonneOrStudentOrProf]

class ClubDetailView(generics.RetrieveAPIView):
    queryset = Club.objects.all()
    serializer_class = ClubSerializer
    permission_classes = [IsAbonneOrStudentOrProf]

# Events
class EventListView(generics.ListAPIView):
    queryset = Event.objects.all().order_by("-date")
    serializer_class = EventSerializer
    permission_classes = [IsAbonneOrStudentOrProf]

class EventDetailView(generics.RetrieveAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAbonneOrStudentOrProf]

# Testimonials
class TestimonialListView(generics.ListAPIView):
    queryset = Testimonial.objects.all().order_by("-id")
    serializer_class = TestimonialSerializer
    permission_classes = [IsAbonneOrStudentOrProf]

class TestimonialDetailView(generics.RetrieveAPIView):
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer
    permission_classes = [IsAbonneOrStudentOrProf]

# Gallery
class GalleryListView(generics.ListAPIView):
    queryset = GalleryItem.objects.all().order_by("-date_added")
    serializer_class = GalleryItemSerializer
    permission_classes = [IsAbonneOrStudentOrProf]

class GalleryDetailView(generics.RetrieveAPIView):
    queryset = GalleryItem.objects.all()
    serializer_class = GalleryItemSerializer
    permission_classes = [IsAbonneOrStudentOrProf]
