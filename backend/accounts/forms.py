# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import User
from students.models import Student
from programs.models import Classroom
from academics.models import AcademicYear
from django.contrib.auth import get_user_model

class StudentRegistrationForm(UserCreationForm):
    # Champs User
    email = forms.EmailField(required=True)

    # Champs Student
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    date_of_birth = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}))
    mother_activity = forms.CharField(required=False)
    father_activity = forms.CharField(required=False)
    parent_phone = forms.CharField(required=True)
    parent_email = forms.EmailField(required=False)
    student_phone = forms.CharField(required=False)
    classroom = forms.ModelChoiceField(queryset=Classroom.objects.all())

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["username", "email", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = "student"
        user.is_active = False  # en attente de validation admin
        if commit:
            user.save()
            academic_year = AcademicYear.objects.filter(is_active=True).first()
            Student.objects.create(
                user=user,
                academic_year=academic_year,
                classroom=self.cleaned_data["classroom"],
                first_name=self.cleaned_data["first_name"],
                last_name=self.cleaned_data["last_name"],
                date_of_birth=self.cleaned_data["date_of_birth"],
                mother_activity=self.cleaned_data.get("mother_activity"),
                father_activity=self.cleaned_data.get("father_activity"),
                parent_phone=self.cleaned_data["parent_phone"],
                parent_email=self.cleaned_data.get("parent_email"),
                student_phone=self.cleaned_data.get("student_phone"),
                matricule=f"STU-{user.id}"
            )
        return user
    
User = get_user_model()

class UserRegisterForm(UserCreationForm):
    ROLE_CHOICES = (
        ('student', 'Étudiant'),
        ('professor', 'Professeur'),
        ('membersite', 'Membre du site'),
    )
    role = forms.ChoiceField(choices=ROLE_CHOICES, label="Rôle")

    class Meta:
        model = User
        fields = ("username", "email", "role", "password1", "password2")

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            "first_name", "last_name", "date_of_birth", "academic_year",
            "program", "classroom", "student_phone", "parent_phone",
            "parent_email", "birth_certificate", "last_school_report"
        ]    
