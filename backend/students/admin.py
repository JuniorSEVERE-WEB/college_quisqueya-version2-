from django.contrib import admin
from programs.models import Classroom
from .models import Student
from django import forms
from django.urls import reverse
from django.utils.html import format_html
from django.core.mail import EmailMessage
from reports.views import student_report_pdf

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
    actions = ["send_report_card_email", "deactivate_students"]

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

    def send_report_card_email(self, request, queryset):
        for student in queryset:
            pdf_response = student_report_pdf(request, student.id)
            pdf_content = pdf_response.content

            email = EmailMessage(
                subject="Your Report Card",
                body="Please find attached your individual report card.",
                to=[student.user.email],
            )
            email.attach(f"ReportCard_{student.first_name}_{student.last_name}.pdf", pdf_content, "application/pdf")
            email.send()
        self.message_user(request, "Report cards sent to selected students.")

    send_report_card_email.short_description = "Send report card to selected students by email"

    def deactivate_students(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, "Selected students have been deactivated.")

    deactivate_students.short_description = "Deactivate selected students"