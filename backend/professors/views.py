from rest_framework import viewsets, permissions
from academics.models import AcademicYear
from .models import Professor
from .serializers import ProfessorSerializer

from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import ProfessorRegisterForm, ProfessorProfileForm

class ProfessorViewSet(viewsets.ModelViewSet):
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        active = AcademicYear.objects.filter(is_active=True).first()
        if active:
            return Professor.objects.filter(academic_year=active).select_related("user", "academic_year")
        return Professor.objects.none()

def professor_register(request):
    if request.method == "POST":
        user_form = ProfessorRegisterForm(request.POST, request.FILES)
        profile_form = ProfessorProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.role = "professor"
            user.is_active = False  # En attente de validation admin
            user.save()
            professor = profile_form.save(commit=False)
            professor.user = user
            professor.save()
            profile_form.save_m2m()
            return render(request, "professors/registration_pending.html")
    else:
        user_form = ProfessorRegisterForm()
        profile_form = ProfessorProfileForm()
    return render(request, "professors/register.html", {
        "user_form": user_form,
        "profile_form": profile_form,
    })