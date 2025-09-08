from django.contrib import admin
from .models import Professor

@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ("user", "program", "subjects")
    filter_horizontal = ("classrooms",)