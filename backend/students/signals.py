# students/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import User
from .models import Student
from academics.models import AcademicYear

@receiver(post_save, sender=User)
def create_student_profile(sender, instance, created, **kwargs):
    if created and instance.role == "student":
        academic_year = AcademicYear.objects.filter(is_active=True).first()  # année active
        if academic_year:
            Student.objects.create(
                user=instance,
                academic_year=academic_year,
                classroom=None,  # choisi après inscription
                first_name=instance.first_name,
                last_name=instance.last_name,
                matricule=f"STU-{instance.id}"
            )

            #Tu peux améliorer : soit demander la classroom dès l’inscription, soit laisser l’admin assigner.
