from django.contrib import admin
from programs.models import Classroom
from .models import Student
from django import forms

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = "__all__"

    class Media:
        js = ("js/filter_classrooms.js",)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "academic_year", "classroom", "user_status")
    list_filter = ("academic_year", "classroom")

    def user_status(self, obj):
        return "✅ Actif" if obj.user.is_active else "⏳ En attente"
    user_status.short_description = "Statut du compte"