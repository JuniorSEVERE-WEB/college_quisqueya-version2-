from django.contrib import admin
from .models import Program, Classroom

class ClassroomInline(admin.TabularInline):
    model = Classroom
    extra = 0
    ordering = ("name",)




@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ("get_name_display", "academic_year", "created_at")
    list_filter = ("academic_year", "name")
    inlines = [ClassroomInline]

    def get_name_display(self, obj):
        return obj.get_name_display()
    get_name_display.short_description = "Programme"

@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ("name", "program", "created_at")
    list_filter = ("program__name", "program__academic_year")
    search_fields = ("name", "program__name")
