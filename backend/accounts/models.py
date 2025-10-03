from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    photo = models.ImageField(
        upload_to="profiles/",
        blank=True,
        null=True,
        verbose_name="Photo de profil"
    )
    email = models.EmailField(
        unique=True,
        blank=False,
        null=False,
        verbose_name="Adresse email"
    )

    # 🔹 Nouveau champ téléphone
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Téléphone"
    )

    # 🔹 Champ sexe
    SEXE_CHOICES = [
        ('homme', 'Homme'),
        ('femme', 'Femme'),
    ]
    sexe = models.CharField(
        max_length=10,
        choices=SEXE_CHOICES,
        blank=True,   # pour ne pas casser les anciens comptes
        null=True,
        verbose_name="Sexe"
    )

    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('prof', 'Professeur'),
        ('student', 'Étudiant'),
        ('employee', 'Employé'),
        ('alumni_student', 'Ancien Étudiant'),
        ('alumni_prof', 'Ancien Professeur'),
        ('alumni_employee', 'Ancien Employé'),
        ('abonne', 'Abonné(e)'),
    ]
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='abonne'
    )

    def save(self, *args, **kwargs):
        if self.role == "abonne":
            self.is_active = True
        else:
            if not self.pk:
                self.is_active = False
        super().save(*args, **kwargs)
