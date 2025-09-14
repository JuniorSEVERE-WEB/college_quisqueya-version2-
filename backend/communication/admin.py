from django.contrib import admin
from .models import Message

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("subject", "sender", "created_at")
    search_fields = ("subject", "body", "sender__username")
    list_filter = ("created_at",)
    filter_horizontal = ("recipients", "read_by")