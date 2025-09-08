from django.db import models
from accounts.models import User
from academics.models import AcademicYear

class Employee(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="employee_profile",
        limit_choices_to={'role': 'employee'}
    )
    academic_year = models.ForeignKey(
        AcademicYear,
        on_delete=models.CASCADE,
        help_text="Année académique en cours"
    )
    position = models.CharField(
        max_length=100,
        help_text="Poste occupé (ex: secrétaire, comptable, surveillant, etc.)"
    )
    hire_date = models.DateField(
        help_text="Date d'embauche"
    )
    department = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Département (optionnel)"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.position} ({self.academic_year})"