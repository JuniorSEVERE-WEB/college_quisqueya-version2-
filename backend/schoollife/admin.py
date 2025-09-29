from django.contrib import admin
from .models import Club, Event, Testimonial, GalleryItem

@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description")
    search_fields = ("name", "description")

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "date", "club")
    list_filter = ("date", "club")
    search_fields = ("title", "description")

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "role")
    search_fields = ("name", "role", "message")

@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "date_added")
    search_fields = ("title",)
