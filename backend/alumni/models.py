from django.db import models
from accounts.models import User

class Alumni(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    year_left = models.PositiveIntegerField(help_text="Année de départ de l'école")
    promo_name = models.CharField(max_length=100, help_text="Nom de la promotion")
    years_interval = models.CharField(
        max_length=20,
        help_text="Intervalle de temps passé à l'école (ex: 2018-2025)"
    )
    proof_document = models.FileField(
        upload_to="alumni_docs/",
        blank=True,
        null=True,
        help_text="Document prouvant le passage à l'école"
    )
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - Alumni ({self.year_left})"
