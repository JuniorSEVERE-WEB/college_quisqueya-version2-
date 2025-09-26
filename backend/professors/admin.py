from django.contrib import admin
from .models import Professor

@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ("id", "get_first_name", "get_last_name", "department", "get_subjects", "hire_date")
    filter_horizontal = ("subjects",)

    def get_first_name(self, obj):
        return obj.user.first_name
    get_first_name.short_description = "Prénom"

    def get_last_name(self, obj):
        return obj.user.last_name
    get_last_name.short_description = "Nom"

    def get_subjects(self, obj):
        return ", ".join([s.name for s in obj.subjects.all()])
    get_subjects.short_description = "Matières"
