from django.contrib import admin
from .models import Employee

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("user", "position", "academic_year", "hire_date", "department", "created_at")
    list_filter = ("academic_year", "position")
    search_fields = ("user__username", "position")
##
    # Pour limiter les choix de user dans l’admin → uniquement role=employee
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        from accounts.models import User
        if db_field.name == "user":
            kwargs["queryset"] = User.objects.filter(role="employee")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
