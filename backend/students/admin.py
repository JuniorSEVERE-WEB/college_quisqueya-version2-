from django.contrib import admin
from programs.models import Classroom
# Register your models here.
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("user", "matricule", "classroom", "academic_year")
    list_filter = ("academic_year", "classroom")
    search_fields = ("user__username", "matricule")

    from .forms import StudentForm
    form = StudentForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # si on ouvre l'URL d'ajout avec ?program=<id>, on filtre les classrooms
        if db_field.name == "classroom":
            program_id = request.GET.get("program")
            if program_id:
                kwargs["queryset"] = Classroom.objects.filter(program_id=program_id)
            else:
                kwargs["queryset"] = Classroom.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def has_change_permission(self, request, obj=None):
        if obj and not obj.academic_year.is_active:
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if obj and not obj.academic_year.is_active:
            return False
        return super().has_delete_permission(request, obj)
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # si on ouvre l'URL d'ajout avec ?program=<id>, on filtre les classrooms
        if db_field.name == "classroom":
            program_id = request.GET.get("program")
            if program_id:
                kwargs["queryset"] = Classroom.objects.filter(program_id=program_id)
            else:
                kwargs["queryset"] = Classroom.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

