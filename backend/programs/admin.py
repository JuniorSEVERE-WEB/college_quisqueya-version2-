from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Program, Classroom, Subject
from students.models import Student


# --- Inline pour les élèves (lecture seule, déjà fait par toi) ---
class StudentInline(admin.TabularInline):
    model = Student
    extra = 0
    fields = ("first_name", "last_name", "student_phone")
    show_change_link = True
    can_delete = True  # L'admin peut supprimer un élève
    readonly_fields = ("first_name", "last_name", "student_phone")  # Lecture seule

    def has_add_permission(self, request, obj=None):
        return False  # Empêche l'ajout d'élèves depuis l'admin de la classe


# --- Inline pour afficher les classes dans Program (avec lien cliquable) ---
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


# --- Inline pour les matières dans une classe ---
class SubjectInline(admin.TabularInline):
    model = Subject
    extra = 1  # permet d’ajouter plusieurs matières rapidement
    fields = ("name",)
    show_change_link = True


# --- Admin Program ---
@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ("name",)
    inlines = [ClassroomLinkInline]


# --- Admin Classroom ---
@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ("name", "program")
    list_display_links = ("name",)
    inlines = [StudentInline, SubjectInline]  # Ajout des élèves + matières


# --- Admin Subject (indépendant, pour une vue globale) ---
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name", "classroom", "get_program")
    list_filter = ("classroom__program", "classroom")
    search_fields = ("name", "classroom__name")

    def get_program(self, obj):
        return obj.classroom.program
    get_program.short_description = "Programme"
