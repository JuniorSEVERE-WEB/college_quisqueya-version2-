from django.contrib import admin
from .models import Club, Event

@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ("name", "description")

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "date")
    list_filter = ("date",)
