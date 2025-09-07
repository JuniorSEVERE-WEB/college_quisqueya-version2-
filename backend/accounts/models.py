from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.


class User(AbstractUser):
    photo = models.ImageField(upload_to="profiles/", blank=True, null=True, verbose_name="Photo de profil")
    email = models.EmailField(unique=True, blank=False, null=False, verbose_name="Adresse email")
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

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='membersite')

    def save(self, *args, **kwargs):
        # Validation automatique pour membership
        if self.role == "membersite":
            self.is_active = True
        else:
            # Les autres attendent l'activation admin
            if not self.pk:  # si c’est une nouvelle inscription
                self.is_active = False
        super().save(*args, **kwargs)
