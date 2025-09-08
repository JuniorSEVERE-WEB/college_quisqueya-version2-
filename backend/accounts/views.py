from django.shortcuts import render, redirect
from django.contrib.auth import login
from accounts.forms import UserRegisterForm, StudentForm
from professors.forms import ProfessorProfileForm
from employees.forms import EmployeeForm  # <-- Ajout import du formulaire employé

def register(request):
    if request.method == "POST":
        user_form = UserRegisterForm(request.POST, request.FILES)
        student_form = StudentForm(request.POST, request.FILES)
        professor_form = ProfessorProfileForm(request.POST)
        employee_form = EmployeeForm(request.POST)  # <-- Ajout du formulaire employé
        if user_form.is_valid():
            user = user_form.save(commit=False)
            if user.role == "student":
                user.is_active = False
            elif user.role == "professor":
                user.is_active = False
            elif user.role == "employee":
                user.is_active = False
            else:
                user.is_active = True
            user.save()
            # Profil étudiant
            if user.role == "student" and student_form.is_valid():
                student = student_form.save(commit=False)
                student.user = user
                student.first_name = user.first_name
                student.last_name = user.last_name
                student.save()
            # Profil professeur
            if user.role == "professor" and professor_form.is_valid():
                professor = professor_form.save(commit=False)
                professor.user = user
                professor.save()
                professor_form.save_m2m()
            # Profil employé
            if user.role == "employee" and employee_form.is_valid():
                employee = employee_form.save(commit=False)
                employee.user = user
                employee.save()
            # Connexion automatique si membre du site
            if user.role == "membersite":
                login(request, user)
                return redirect("membersite_dashboard")
            return render(request, "accounts/registration_pending.html")
    else:
        user_form = UserRegisterForm()
        student_form = StudentForm()
        professor_form = ProfessorProfileForm()
        employee_form = EmployeeForm()  # <-- Ajout du formulaire employé
    return render(request, "accounts/register.html", {
        "user_form": user_form,
        "student_form": student_form,
        "professor_form": professor_form,
        "employee_form": employee_form,  # <-- Ajout
    })