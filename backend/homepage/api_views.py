from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import Slide, Welcome, Value
from .serializers import SlideSerializer, WelcomeSerializer, ValueSerializer


# Slides du carrousel
class SlideListView(generics.ListAPIView):
    queryset = Slide.objects.all().order_by("id")
    serializer_class = SlideSerializer
    permission_classes = [AllowAny]


# Section de bienvenue (souvent un seul objet)
class WelcomeListView(generics.ListAPIView):
    queryset = Welcome.objects.all()
    serializer_class = WelcomeSerializer
    permission_classes = [AllowAny]


# Valeurs & missions
class ValueListView(generics.ListAPIView):
    queryset = Value.objects.all().order_by("id")
    serializer_class = ValueSerializer
    permission_classes = [AllowAny]
