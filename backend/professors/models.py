from django.db import models

# Create your models here.
from accounts.models import User
from academics.models import AcademicYear

class Professor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="professor_profile")
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    department = models.CharField(max_length=100, blank=True, null=True)
    hire_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "academic_year")  # Un prof ne peut exister qu’une fois par année
        ordering = ["user__username"]

    def __str__(self):
        return f"{self.user.username} ({self.academic_year})"
