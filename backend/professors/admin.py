from django.contrib import admin
from .models import Professor

@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
	list_display = ("user", "department", "academic_year", "hire_date")
	list_filter = ("academic_year", "department")
	
