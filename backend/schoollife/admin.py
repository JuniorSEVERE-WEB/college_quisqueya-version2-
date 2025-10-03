from django.contrib import admin
from django.utils.html import format_html
from .models import Club, Event, Testimonial, GalleryItem


# --- Helper pour afficher les images dans l’admin ---
def image_preview(obj, field_name="photo", size=50):
    field = getattr(obj, field_name, None)
    if field and getattr(field, "url", None):
        return format_html(f'<img src="{field.url}" width="{size}" height="{size}" style="object-fit:cover;border-radius:6px;"/>')
    return "—"
image_preview.short_description = "Preview"


# --- Clubs ---
@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ("name", "photo_preview", "description")
    search_fields = ("name", "description")

    def photo_preview(self, obj):
        return image_preview(obj, "photo")
    photo_preview.short_description = "Photo"


# --- Events ---
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "club", "date", "logo_preview")
    list_filter = ("date", "club")
    search_fields = ("title", "description")

    def logo_preview(self, obj):
        return image_preview(obj, "logo")
    logo_preview.short_description = "Logo"


# --- Testimonials ---
@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("name", "role", "photo_preview", "message")
    search_fields = ("name", "role", "message")

    def photo_preview(self, obj):
        return image_preview(obj, "photo")
    photo_preview.short_description = "Photo"


# --- Gallery ---
@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ("title", "image_preview", "date_added")
    search_fields = ("title",)
    list_filter = ("date_added",)

    def image_preview(self, obj):
        return image_preview(obj, "image")
    image_preview.short_description = "Image"
