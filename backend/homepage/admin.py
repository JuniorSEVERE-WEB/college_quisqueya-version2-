from django.contrib import admin
from .models import Slide, SlideTitle, Welcome, Value


class SlideTitleInline(admin.TabularInline):
    model = SlideTitle
    extra = 1   # affiche au moins 1 champ vide par défaut


@admin.register(Slide)
class SlideAdmin(admin.ModelAdmin):
    list_display = ("id", "text", "image")
    search_fields = ("text",)
    list_per_page = 10
    inlines = [SlideTitleInline]


@admin.register(Welcome)
class WelcomeAdmin(admin.ModelAdmin):
    list_display = ("id", "title")
    search_fields = ("title", "content")


@admin.register(Value)
class ValueAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "icon")
    list_filter = ("icon",)
    search_fields = ("title", "description")
