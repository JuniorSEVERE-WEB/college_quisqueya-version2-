from django.shortcuts import render, redirect
from django.contrib.auth import login
from accounts.forms import UserRegisterForm, StudentForm

def register(request):
    if request.method == "POST":
        user_form = UserRegisterForm(request.POST)
        student_form = StudentForm(request.POST, request.FILES)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            if user.role == "student":
                user.is_active = False
            else:
                user.is_active = True
            user.save()
            # Automatisme : copie first_name et last_name dans le profil Student
            if user.role == "student" and student_form.is_valid():
                student = student_form.save(commit=False)
                student.user = user
                student.first_name = user.first_name
                student.last_name = user.last_name
                student.save()
            if user.role == "membersite":
                # Si tu as un modèle Membersite, fais pareil ici
                pass
            if user.role == "membersite":
                login(request, user)
                return redirect("membersite_dashboard")
            return render(request, "accounts/registration_pending.html")
    else:
        user_form = UserRegisterForm()
        student_form = StudentForm()
    return render(request, "accounts/register.html", {
        "user_form": user_form,
        "student_form": student_form,
    })