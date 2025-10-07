from django.db import models
from accounts.models import User
from academics.models import AcademicYear
from programs.models import Classroom


class Student(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="student_profile",
        limit_choices_to={'role': 'student'}
    )
    academic_year = models.ForeignKey(
        AcademicYear,
        on_delete=models.CASCADE,
        help_text="Année académique de l'étudiant"
    )
    classroom = models.ForeignKey(
        Classroom,
        on_delete=models.CASCADE,
        help_text="Classe assignée"
    )
    father_job = models.CharField(max_length=100, blank=True, null=True, default="Non renseigné")
    mother_job = models.CharField(max_length=100, blank=True, null=True, default="Non renseigné")


    # 🔹 Nouveaux champs facultatifs (aucune perte de données)
    

    birth_certificate = models.FileField(
        upload_to="students/certificates/",
        blank=True,
        null=True,
        help_text="Certificat de naissance (PDF max 3MB)"
    )
    last_school_report = models.FileField(
        upload_to="students/reports/",
        blank=True,
        null=True,
        help_text="Bulletin de la dernière école (PDF max 3MB)"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.classroom.name}"
