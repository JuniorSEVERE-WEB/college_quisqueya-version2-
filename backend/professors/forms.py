from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import User
from .models import Professor, Program, Classroom

class ProfessorRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "photo", "password1", "password2")

class ProfessorProfileForm(forms.ModelForm):
    class Meta:
        model = Professor
        fields = ("program", "subjects", "classrooms", "department", "hire_date", "academic_year")
        widgets = {
            "subjects": forms.TextInput(attrs={"placeholder": "Maths, Physique, Chimie"}),
            "classrooms": forms.SelectMultiple(),
            "hire_date": forms.DateInput(attrs={"type": "date"}),
        }