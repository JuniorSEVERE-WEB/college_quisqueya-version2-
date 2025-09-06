from django.db import models
from django.conf import settings
from academics.models import AcademicYear
from programs.models import Classroom

class Student(models.Model):
    last_school = models.CharField(max_length=200, blank=True, null=True, verbose_name="Dernière école fréquentée")
    mother_activity = models.CharField(max_length=200, blank=True, null=True, verbose_name="Activité de la mère")
    father_activity = models.CharField(max_length=200, blank=True, null=True, verbose_name="Activité du père")
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="student_profile")
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.PROTECT, related_name="students")
    first_name = models.CharField(max_length=100, default="Unknown")
    last_name = models.CharField(max_length=100, default="Unknown")
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, null=True, blank=True)
    matricule = models.CharField(max_length=50, unique=True)
    date_of_birth = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Nouveau champs pour les contacts
    student_phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Téléphone de l'élève")
    parent_phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Téléphone du parent")
    parent_email = models.EmailField(blank=True, null=True, verbose_name="Email du parent")

    # Fichiers à télécharger
    birth_certificate = models.FileField(upload_to="students/birth_certificates/", blank=True, null=True, verbose_name="Extrait d'archive (Acte de naissance)")
    last_school_report = models.FileField(upload_to="students/last_school_reports/", blank=True, null=True, verbose_name="Dernier carnet scolaire")

    class Meta:
        unique_together = ("user", "academic_year")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
