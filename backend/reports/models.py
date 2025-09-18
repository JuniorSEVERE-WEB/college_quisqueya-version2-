from django.db import models
from django.conf import settings
from smart_selects.db_fields import ChainedForeignKey
from programs.models import Classroom, Subject, Program
from academics.models import AcademicYear
from students.models import Student


# ---------- ReportSession ----------
from django.db import models
from django.conf import settings

TRIMESTER_CHOICES = [
    ('T1', 'Trimestre 1'),
    ('T2', 'Trimestre 2'),
    ('T3', 'Trimestre 3'),
]

STEP_CHOICES = [
    ('S1', 'Etape 1'),
    ('S2', 'Etape 2'),
    ('S3', 'Etape 3'),
    ('S4', 'Etape 4'),
    ('S5', 'Etape 5'),
]

class ReportSession(models.Model):
    title = models.CharField(max_length=200, blank=True)
    classroom = models.ForeignKey('programs.Classroom', on_delete=models.CASCADE, related_name='report_sessions')
    academic_year = models.ForeignKey('academics.AcademicYear', on_delete=models.CASCADE, related_name='report_sessions')
    trimester = models.CharField(max_length=2, choices=TRIMESTER_CHOICES)
    step = models.CharField(max_length=2, choices=STEP_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        limit_choices_to={'is_staff': True}
    )
    is_active = models.BooleanField(default=False)  # ✅ nouvelle colonne pour session active

    class Meta:
        unique_together = ('classroom', 'academic_year', 'trimester', 'step')
        ordering = ['-created_at']

    def __str__(self):
        title = self.title or "Report"
        return f"{self.classroom.name} • {self.academic_year} • {self.get_trimester_display()} • {self.get_step_display()} • {title}"

    def save(self, *args, **kwargs):
        # Forcer un seul actif à la fois
        if self.is_active:
            ReportSession.objects.filter(is_active=True).exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)

    @staticmethod
    def get_active_session():
        """Retourne la session active actuelle, ou None"""
        return ReportSession.objects.filter(is_active=True).first()  


# ---------- SubjectCoefficient ----------
class SubjectCoefficient(models.Model):
    """
    Coefficient fixé POUR UNE ANNÉE pour une matière dans une classe.
    Exemple : (classroom=3A, subject=Math, academic_year=2025-2026, coefficient=300)
    Ces coefficients sont saisis une fois et réutilisés.
    """
    classroom = models.ForeignKey('programs.Classroom', on_delete=models.CASCADE, related_name='subject_coefficients')
    subject = models.ForeignKey('programs.Subject', on_delete=models.CASCADE, related_name='subject_coefficients')
    academic_year = models.ForeignKey('academics.AcademicYear', on_delete=models.CASCADE, related_name='subject_coefficients')
    coefficient = models.PositiveIntegerField(default=100)

    class Meta:
        unique_together = ('classroom', 'subject', 'academic_year')

    def __str__(self):
        return f"{self.subject.name} — {self.classroom.name} ({self.academic_year}) = {self.coefficient}"
from smart_selects.db_fields import ChainedForeignKey

class Grade(models.Model):
    program = models.ForeignKey('programs.Program', on_delete=models.CASCADE)
    classroom = ChainedForeignKey(
        'programs.Classroom',
        chained_field="program",
        chained_model_field="program",
        show_all=False,
        auto_choose=True,
        sort=True,
        on_delete=models.CASCADE
    )
    student = ChainedForeignKey(
        'students.Student',
        chained_field="classroom",
        chained_model_field="classroom",
        show_all=False,
        auto_choose=True,
        sort=True,
        on_delete=models.CASCADE
    )
    subject = ChainedForeignKey(
        'programs.Subject',
        chained_field="classroom",
        chained_model_field="classroom",
        show_all=False,
        auto_choose=True,
        sort=True,
        on_delete=models.CASCADE
    )
    report_session = ChainedForeignKey(
        'reports.ReportSession',
        chained_field="classroom",
        chained_model_field="classroom",
        show_all=False,
        auto_choose=True,
        sort=True,
        on_delete=models.CASCADE
    )
    note = models.FloatField()