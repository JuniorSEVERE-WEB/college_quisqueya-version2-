# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login
from accounts.forms import StudentRegistrationForm
from .forms import UserRegisterForm, StudentForm

def student_register(request):
    if request.method == "POST":
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect("registration_pending")
    else:
        form = StudentRegistrationForm()
    return render(request, "accounts/student_register.html", {"form": form})


def register_student(request):
    if request.method == "POST":
        user_form = UserRegisterForm(request.POST)
        student_form = StudentForm(request.POST, request.FILES)
        if user_form.is_valid() and student_form.is_valid():
            user = user_form.save(commit=False)
            user.is_active = False  # ⚠️ mettre en attente
            user.save()
            student = student_form.save(commit=False)
            student.user = user
            student.save()
            return render(request, "accounts/registration_pending.html")
    else:
        user_form = UserRegisterForm()
        student_form = StudentForm()
    return render(request, "accounts/student_register.html", {
        "user_form": user_form,
        "student_form": student_form,
    })
