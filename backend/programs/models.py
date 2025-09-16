# programs/models.py
from django.db import models
from academics.models import AcademicYear


class Program(models.Model):
    KINDERGARTEN = "KINDERGARTEN"
    PRIMAIRE = "PRIMAIRE"
    SECONDAIRE = "SECONDAIRE"

    PROGRAM_CHOICES = [
        (KINDERGARTEN, "Kindergarten"),
        (PRIMAIRE, "Primaire"),
        (SECONDAIRE, "Secondaire"),
    ]

    name = models.CharField(max_length=50, choices=PROGRAM_CHOICES, unique=True)

    def __str__(self):
        return self.get_name_display()


class Classroom(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name="classrooms")
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.program.get_name_display()})"
    

# programs/models.py
class Subject(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name="subjects")
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ("classroom", "name")  # éviter doublons

    def __str__(self):
        return f"{self.name} - {self.classroom.name}"
