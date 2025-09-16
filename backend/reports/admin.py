from django.contrib import admin
from django import forms
from .models import ReportSession, Grade, SubjectCoefficient

@admin.register(ReportSession)
class ReportSessionAdmin(admin.ModelAdmin):
    list_display = ("title", "classroom", "academic_year", "trimester", "step", "created_by")
    list_filter = ("academic_year", "classroom", "trimester", "step")
    search_fields = ("title",)
    exclude = ("created_by",)  # <-- Ne pas afficher dans le formulaire

    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ("student", "subject", "note", "report_session")
    list_filter = ("report_session", "subject", "student")
    search_fields = ("student__first_name", "student__last_name", "subject__name")

@admin.register(SubjectCoefficient)
class SubjectCoefficientAdmin(admin.ModelAdmin):
    list_display = ("subject", "classroom", "academic_year", "coefficient")
    list_filter = ("classroom", "academic_year", "subject")
    search_fields = ("subject__name", "classroom__name")