from django.contrib import admin
from .models import Message, ContactMessage


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("subject", "sender", "created_at")
    search_fields = ("subject", "body", "sender__username")
    list_filter = ("created_at",)
    filter_horizontal = ("recipients", "read_by")


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "created_at", "is_read")
    search_fields = ("name", "email", "subject", "message")
    list_filter = ("created_at", "is_read")
