# accounts/forms.py
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm as DjangoUserCreationForm, UserChangeForm as DjangoUserChangeForm
from students.models import Student

User = get_user_model()

# Formulaires utilisés par l’admin (hash correct du mot de passe)
class AdminUserCreationForm(DjangoUserCreationForm):
    class Meta(DjangoUserCreationForm.Meta):
        model = User
        fields = ("username", "email", "first_name", "last_name")

class AdminUserChangeForm(DjangoUserChangeForm):
    class Meta(DjangoUserChangeForm.Meta):
        model = User
        fields = (
            "username", "email", "first_name", "last_name",
            "is_active", "is_staff", "is_superuser", "groups", "user_permissions"
        )

# Formulaire d’inscription côté site
class UserRegisterForm(DjangoUserCreationForm):
    class Meta(DjangoUserCreationForm.Meta):
        model = User
        fields = ("username", "email", "password1", "password2")

# Formulaire Student sans champs inconnus
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        exclude = ("user",)  # on lie user dans la vue