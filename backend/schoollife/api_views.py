from rest_framework import generics
from .models import Club, Event
from .serializers import ClubSerializer, EventSerializer


# --- Clubs ---
class ClubListView(generics.ListAPIView):
    queryset = Club.objects.all()
    serializer_class = ClubSerializer


class ClubDetailView(generics.RetrieveAPIView):
    queryset = Club.objects.all()
    serializer_class = ClubSerializer


# --- Events ---
class EventListView(generics.ListAPIView):
    queryset = Event.objects.all().order_by("-date")  # derniers d'abord
    serializer_class = EventSerializer


class EventDetailView(generics.RetrieveAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
