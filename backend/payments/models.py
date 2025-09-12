from django.db import models
from django.conf import settings
from academics.models import AcademicYear

# 1. Frais d’inscription
class EnrollmentFee(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="fees")
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_paid = models.DateTimeField(auto_now_add=True)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"Frais {self.student} - {self.academic_year} - {self.amount} Gdes"


# 2. Dons
class Donation(models.Model):
    donor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="donations"
    )  # si donateur connecté
    name = models.CharField(max_length=200, blank=True)  # si anonyme
    email = models.EmailField(blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    message = models.TextField(blank=True, null=True)
    date_donated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Don {self.name or self.donor} - {self.amount} Gdes"


# 3. Historique des transactions (lié à tout type)
class Transaction(models.Model):
    PAYMENT_TYPES = [
        ("enrollment", "Frais d’inscription"),
        ("donation", "Don"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPES)
    reference_id = models.PositiveIntegerField()  # ID de l’objet lié (EnrollmentFee ou Donation)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default="completed")  # completed / pending / failed

    def __str__(self):
        return f"{self.payment_type} - {self.amount} Gdes - {self.status}"
