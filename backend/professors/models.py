from django.db import models
from accounts.models import User
from academics.models import AcademicYear
from programs.models import Program, Classroom

class Professor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="professor_profile")
    academic_year = models.ForeignKey(
        AcademicYear,
        on_delete=models.CASCADE,
        help_text="Année académique active choisie par le professeur"
    )
    
    program = models.ForeignKey(
    Program,
    on_delete=models.CASCADE,
    help_text="Programme auquel le professeur appartient (à choisir parmi les programmes enregistrés)"
    )

    department = models.CharField(max_length=100, blank=True, null=True)
    hire_date = models.DateField(blank=True, null=True)
    subjects = models.CharField(
        max_length=255,
        help_text="Liste des matières enseignées, séparées par des virgules (à saisir par le professeur)"
    )
    classrooms = models.ManyToManyField(
        Classroom,
        help_text="Classes déjà enregistrées, à choisir par le professeur"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "academic_year")
        ordering = ["user__username"]

    def __str__(self):
        return f"{self.user.username} ({self.academic_year})"