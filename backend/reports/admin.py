from django.contrib import admin
from django import forms
from .models import ReportSession, Grade, SubjectCoefficient
from django.urls import reverse
from django.utils.html import format_html
from students.models import Student


@admin.register(ReportSession)
class ReportSessionAdmin(admin.ModelAdmin):
    list_display = (
        "title", "classroom", "academic_year",
        "trimester", "step", "is_active", "created_at", "created_by"
    )
    list_filter = ("academic_year", "classroom", "trimester", "step", "is_active")
    search_fields = ("title", "classroom__name", "academic_year__name")
    list_editable = ("is_active",)

    actions = ["make_active"]

    def save_model(self, request, obj, form, change):
        if obj.is_active:
            # ⚡ si on active cette session, les autres sont désactivées
            ReportSession.objects.exclude(pk=obj.pk).update(is_active=False)
        obj.created_by = obj.created_by or request.user
        super().save_model(request, obj, form, change)

    def make_active(self, request, queryset):
        """Action admin pour activer une session et désactiver les autres"""
        if queryset.count() == 1:
            session = queryset.first()
            ReportSession.objects.exclude(pk=session.pk).update(is_active=False)
            session.is_active = True
            session.save()
            self.message_user(request, f"La session {session} a été activée ✅")
        else:
            self.message_user(request, "Sélectionne exactement UNE session à activer ⚠️")
    make_active.short_description = "Activer la session sélectionnée"

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

