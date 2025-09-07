# students/models.py
from django.db import models
from django.conf import settings
from academics.models import AcademicYear
from programs.models import Classroom

class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="student_profile")
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.PROTECT, related_name="students")
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)

    # Infos perso
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(blank=True, null=True)

    # Infos parent
    mother_activity = models.CharField(max_length=200, blank=True, null=True)
    father_activity = models.CharField(max_length=200, blank=True, null=True)
    parent_phone = models.CharField(max_length=20, blank=True, null=True)
    parent_email = models.EmailField(blank=True, null=True)

    # Autres
    last_school = models.CharField(max_length=200, blank=True, null=True)
    student_phone = models.CharField(max_length=20, blank=True, null=True)
    matricule = models.CharField(max_length=50, unique=True)
    birth_certificate = models.FileField(upload_to="students/birth_certificates/", blank=True, null=True)
    last_school_report = models.FileField(upload_to="students/last_school_reports/", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "academic_year")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.user.username})"
