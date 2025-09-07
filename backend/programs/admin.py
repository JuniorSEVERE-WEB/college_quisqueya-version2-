from django.contrib import admin

from .models import Program, Classroom

class ClassroomInline(admin.TabularInline):
    model = Classroom
    extra = 1

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ("name",)
    inlines = [ClassroomInline]

@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ("name", "program")
    list_filter = ("program",)

