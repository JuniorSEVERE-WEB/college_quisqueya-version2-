from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('prof', 'Professeur'),
        ('student', 'Étudiant'),
        ('employee', 'Employé'),
        ('alumni_student', 'Ancien Étudiant'),
        ('alumni_prof', 'Ancien Professeur'),
        ('alumni_employee', 'Ancien Employé'),
        ('membersite', 'Membre du site'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
