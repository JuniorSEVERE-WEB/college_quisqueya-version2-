from django.contrib import admin
from .models import Alumni

@admin.register(Alumni)
class AlumniAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "year_left", "promo_name", "years_interval", "date_created")
    search_fields = ("user__username", "promo_name")
    list_filter = ("role", "year_left")
    actions = ["make_alumni"]

    def make_alumni(self, request, queryset):
        for alumni in queryset:
            alumni.role = "student"  # exemple, à adapter selon le contexte
            alumni.save()
    make_alumni.short_description = "Basculer en alumni"