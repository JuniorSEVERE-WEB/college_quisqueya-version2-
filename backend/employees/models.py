from django.db import models

# Create your models here.
from accounts.models import User
from academics.models import AcademicYear

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'role': 'employee'})
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    position = models.CharField(max_length=100)  # poste de l'employé
    hire_date = models.DateField()  # date d'embauche
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} ({self.position})"