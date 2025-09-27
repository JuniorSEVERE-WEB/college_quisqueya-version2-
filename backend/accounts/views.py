from django.shortcuts import render, redirect
from django.contrib.auth import login
from accounts.forms import UserRegisterForm, StudentForm
from professors.forms import ProfessorProfileForm
from employees.forms import EmployeeForm


def register(request):
    if request.method == "POST":
        user_form = UserRegisterForm(request.POST, request.FILES)
        student_form = StudentForm(request.POST, request.FILES)
        professor_form = ProfessorProfileForm(request.POST)
        employee_form = EmployeeForm(request.POST)

        if user_form.is_valid():
            # UserCreationForm a déjà set_password() même avec commit=False
            user = user_form.save(commit=False)

            # Politique d’activation
            if user.role in ("student", "prof", "employee"):
                user.is_active = False
            else:
                user.is_active = True

            # Par sécurité, on reforce le hash si besoin
            try:
                pwd = user_form.cleaned_data.get("password1")
                if pwd:
                    user.set_password(pwd)
            except Exception:
                pass

            user.save()

            # Profils liés
            if user.role == "student" and student_form.is_valid():
                student = student_form.save(commit=False)
                student.user = user
                student.first_name = getattr(user, "first_name", student.first_name)
                student.last_name = getattr(user, "last_name", student.last_name)
                student.save()

            if user.role == "prof" and professor_form.is_valid():
                professor = professor_form.save(commit=False)
                professor.user = user
                professor.save()
                professor_form.save_m2m()

            if user.role == "employee" and employee_form.is_valid():
                employee = employee_form.save(commit=False)
                employee.user = user
                employee.save()

            # Connexion auto pour abonné
            if user.role == "abonne" and user.is_active:
                login(request, user)
                return redirect("membersite_dashboard")

            return render(request, "accounts/registration_pending.html")

    else:
        user_form = UserRegisterForm()
        student_form = StudentForm()
        professor_form = ProfessorProfileForm()
        employee_form = EmployeeForm()

    return render(request, "accounts/register.html", {
        "user_form": user_form,
        "student_form": student_form,
        "professor_form": professor_form,
        "employee_form": employee_form,
    })
