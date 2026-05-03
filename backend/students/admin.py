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
    search_fields = ("user__first_name", "user__last_name", "user__email")
    actions = ["send_report_card_email", "deactivate_students"]

    # 🔹 méthodes pour accéder aux infos du User lié
    def first_name(self, obj):
        return obj.user.first_name
    first_name.admin_order_field = "user__first_name"
    first_name.short_description = "Prénom"

    def last_name(self, obj):
        return obj.user.last_name
    last_name.admin_order_field = "user__last_name"
    last_name.short_description = "Nom"

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

    def send_report_card_email(self, request, queryset):
        for student in queryset:
            pdf_response = student_report_pdf(request, student.id)
            pdf_content = pdf_response.content

            email = EmailMessage(
                subject="Your Report Card",
                body="Please find attached your individual report card.",
                to=[student.user.email],
            )
            # 🔹 on va chercher prénom et nom dans user
            filename = f"ReportCard_{student.user.first_name}_{student.user.last_name}.pdf"
            email.attach(filename, pdf_content, "application/pdf")
            email.send()
        self.message_user(request, "Report cards sent to selected students.")

    send_report_card_email.short_description = "Envoyer bulletin par email aux étudiants sélectionnés"

    def deactivate_students(self, request, queryset):
        for student in queryset:
            student.user.is_active = False
            student.user.save()
        self.message_user(request, "Comptes des étudiants sélectionnés désactivés.")

    deactivate_students.short_description = "Désactiver comptes des étudiants sélectionnés"
