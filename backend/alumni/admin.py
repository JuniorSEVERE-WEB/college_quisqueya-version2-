from django.contrib import admin
from .models import Alumni


@admin.register(Alumni)
class AlumniAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "year_left", "promo_name", "years_interval", "date_created")
    list_filter = ("year_left",)
    search_fields = (
        "promo_name",
        "years_interval",
        "user__first_name",
        "user__last_name",
        "user__email",
    )
    ordering = ("-date_created",)
