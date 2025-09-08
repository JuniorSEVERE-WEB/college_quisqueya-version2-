from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Program, Classroom
from students.models import Student

class StudentInline(admin.TabularInline):
    model = Student
    extra = 0
    fields = ("first_name", "last_name", "student_phone")
    show_change_link = True
    can_delete = True  # L'admin peut supprimer un élève
    readonly_fields = ("first_name", "last_name", "student_phone")  # Lecture seule

    def has_add_permission(self, request, obj=None):
        return False  # Empêche l'ajout d'élèves depuis l'admin de la classe

class ClassroomLinkInline(admin.TabularInline):
    model = Classroom
    extra = 0
    readonly_fields = ("classroom_link",)

    def classroom_link(self, obj):
        if obj.pk:
            url = reverse("admin:programs_classroom_change", args=[obj.pk])
            return format_html('<a href="{}">{}</a>', url, obj.name)
        return ""
    classroom_link.short_description = "Classe (cliquable)"

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ("name",)
    inlines = [ClassroomLinkInline]

@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ("name", "program")
    list_display_links = ("name",)
    inlines = [StudentInline]