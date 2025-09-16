from django.contrib import admin
from .models import (
    AcademicYear, Trimester, Step, Classroom, Subject,
    Professor, Student, Note, Resource, Assignment, Submission
)

@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active")
    list_editable = ("is_active",)
    ordering = ("-id",)
    search_fields = ("name",)
