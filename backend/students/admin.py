from django.contrib import admin

# Register your models here.
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("user", "matricule", "program", "academic_year")
    list_filter = ("academic_year", "program")
    search_fields = ("user__username", "matricule")

    def has_change_permission(self, request, obj=None):
        if obj and not obj.academic_year.is_active:
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if obj and not obj.academic_year.is_active:
            return False
        return super().has_delete_permission(request, obj)

