from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class AcademicYear(models.Model):
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.is_active:
            AcademicYear.objects.exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Trimester(models.Model):
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name="trimesters")
    name = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.name} ({self.academic_year.name})"

class Step(models.Model):
    trimester = models.ForeignKey(
        Trimester, on_delete=models.CASCADE, related_name="steps"
    )
    name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=False)

    def clean(self):
        # Vérifier qu'un trimestre n'a pas plus de 2 étapes
        if self.pk is None and self.trimester.steps.count() >= 2:
            raise ValidationError("Un trimestre ne peut pas avoir plus de 2 étapes.")

    def save(self, *args, **kwargs):
        self.clean()
        if self.is_active:
            Step.objects.filter(trimester=self.trimester).exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.trimester.name})"

class Classroom(models.Model):
    name = models.CharField(max_length=100)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name="classrooms")

    def __str__(self):
        return self.name

class Subject(models.Model):
    name = models.CharField(max_length=100)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name="subjects")
    coefficient = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.name} ({self.classroom.name})"

class Professor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subjects = models.ManyToManyField(Subject, related_name="professors")

    def __str__(self):
        return self.user.get_full_name()

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name="students")

    def __str__(self):
        return self.user.get_full_name()

class Note(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="notes")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="notes")
    step = models.ForeignKey(Step, on_delete=models.CASCADE, related_name="notes")
    value = models.FloatField()

    def __str__(self):
        return f"{self.student} - {self.subject} - {self.value}"

class Resource(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="resources")
    step = models.ForeignKey(Step, on_delete=models.CASCADE, related_name="resources")
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name="resources")
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to="resources/")
    video_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Assignment(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="assignments")
    step = models.ForeignKey(Step, on_delete=models.CASCADE, related_name="assignments")
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name="assignments")
    title = models.CharField(max_length=200)
    due_date = models.DateTimeField()

    def __str__(self):
        return self.title

class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name="submissions")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="submissions")
    file = models.FileField(upload_to="submissions/")
    submitted_at = models.DateTimeField(auto_now_add=True)
    grade = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"{self.student} - {self.assignment}"