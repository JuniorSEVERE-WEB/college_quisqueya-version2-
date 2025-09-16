from django.db import models
from django.conf import settings


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
    step = models.CharField(max_length=2, choices=STEP_CHOICES)  # unique=True retiré
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        limit_choices_to={'is_staff': True}
    )

    class Meta:
        unique_together = ('classroom', 'academic_year', 'trimester', 'step')
        ordering = ['-created_at']

    def __str__(self):
        title = self.title or "Report"
        return f"{self.classroom.name} • {self.academic_year} • {self.get_trimester_display()} • {self.get_step_display()} • {title}"

    def save(self, *args, **kwargs):
        # Si created_by n'est pas défini, on le met automatiquement (si possible)
        if not self.created_by and hasattr(self, '_current_user'):
            self.created_by = self._current_user
        super().save(*args, **kwargs)

    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)    


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


# ---------- Grade ----------
class Grade(models.Model):
    """
    Une note (cellule du tableau) : relie un student, une subject et une ReportSession (donc implicitement année/trimestre/étape).
    On garantit qu'il n'y a qu'une note par (report_session, student, subject).
    """
    report_session = models.ForeignKey(ReportSession, on_delete=models.CASCADE, related_name='grades')
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='grades')
    subject = models.ForeignKey('programs.Subject', on_delete=models.CASCADE, related_name='grades')
    note = models.DecimalField(max_digits=5, decimal_places=2)  # précision : 2 chiffres après la virgule

    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('report_session', 'student', 'subject')
        ordering = ['student__last_name', 'student__first_name']

    def __str__(self):
        return f"{self.student} • {self.subject.name} : {self.note}"
