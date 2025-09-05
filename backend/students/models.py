from django.db import models

# Create your models here.
from django.conf import settings
from academics.models import AcademicYear

class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="student_profile")
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.PROTECT, related_name="students")
    matricule = models.CharField(max_length=50, unique=True)
    program = models.CharField(max_length=100, blank=True, null=True)  # ex: Informatique, Droit
    date_of_birth = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "academic_year")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} - {self.academic_year.name}"
