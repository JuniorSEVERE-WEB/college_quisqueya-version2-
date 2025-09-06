# programs/models.py
from django.db import models
from academics.models import AcademicYear

class Program(models.Model):
    PROGRAM_CHOICES = [
        ("kindergarten", "Kindergarten"),
        ("primaire", "Primaire"),
        ("secondaire", "Secondaire"),
    ]

    name = models.CharField(max_length=20, choices=PROGRAM_CHOICES)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_name_display()} ({self.academic_year.name})"


class Classroom(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name="classrooms")
    name = models.CharField(max_length=50)  # ex: "1e A Kinder", "NS4"
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.program.get_name_display()}"
