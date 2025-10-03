from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Program, Classroom, Subject
from students.models import Student


# --- Inline pour les élèves ---
class StudentInline(admin.TabularInline):
    model = Student
    extra = 0
    fields = ("first_name", "last_name")  # student_phone retiré si inexistant
    readonly_fields = ("first_name", "last_name")
    show_change_link = True
    can_delete = True

    def has_add_permission(self, request, obj=None):
        return False  # Empêche l'ajout d'élèves depuis l'admin de la classe

    # 🔹 méthodes pour afficher prénom et nom depuis User
    def first_name(self, obj):
        return obj.user.first_name
    first_name.admin_order_field = "user__first_name"
    first_name.short_description = "Prénom"

    def last_name(self, obj):
        return obj.user.last_name
    last_name.admin_order_field = "user__last_name"
    last_name.short_description = "Nom"


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
    extra = 1
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
    inlines = [StudentInline, SubjectInline]


# --- Admin Subject ---
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name", "classroom", "get_program")
    list_filter = ("classroom__program", "classroom")
    search_fields = ("name", "classroom__name")

    def get_program(self, obj):
        return obj.classroom.program
    get_program.short_description = "Programme"
