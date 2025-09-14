from django.db import models

# Create your models here.
class AcademicYear(models.Model):
    name = models.CharField(max_length=100, unique=True)  # ex: 2025-2026
    is_active = models.BooleanField(default=False)

    class Meta:
        ordering = ["-id"]

    def save(self, *args, **kwargs):
        if self.is_active:
            # désactiver les autres années
            AcademicYear.objects.exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)

    def __str__(self):
        status = " (Active)" if self.is_active else ""
        return f"{self.name}{status}"
    

class Classroom(models.Model):
    name = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField()
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)

    def __str__(self):
        return self.name