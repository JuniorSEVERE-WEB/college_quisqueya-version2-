from django.contrib import admin
from programs.models import Classroom
from .models import Student
from django import forms
from django.urls import reverse
from django.utils.html import format_html

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = "__all__"

    class Media:
        js = ("js/filter_classrooms.js",)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "classroom", "user_status", "view_report_links")
    list_filter = ("classroom",)
    search_fields = ("first_name", "last_name")

    def user_status(self, obj):
        return "✅ Actif" if obj.user.is_active else "⏳ En attente"
    user_status.short_description = "Statut du compte"

    def view_report_links(self, obj):
        pdf_url = reverse("student_report_pdf", args=[obj.id])
        return format_html(
            '<a class="button" href="{}" target="_blank">PDF</a>',
            pdf_url
        )
    view_report_links.short_description = "Bulletin"
    view_report_links.allow_tags = True