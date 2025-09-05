from django.contrib import admin

# Register your models here.

from .models import AcademicYear

@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active")
    list_editable = ("is_active",)
    ordering = ("-id",)
