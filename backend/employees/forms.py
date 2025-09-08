from django import forms
from .models import Employee

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ("academic_year", "position", "hire_date", "department")
        widgets = {
            "hire_date": forms.DateInput(attrs={"type": "date"}),
        }