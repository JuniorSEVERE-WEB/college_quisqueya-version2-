from django.db import models

class AboutInfo(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    founded_date = models.DateField()
    main_image = models.ImageField(upload_to="about/", blank=True, null=True)

    def __str__(self):
        return self.title


class TimelineEvent(models.Model):
    year = models.CharField(max_length=10)
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to="timeline/", blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.year} - {self.title}"


class Founder(models.Model):
    name = models.CharField(max_length=150)
    role = models.CharField(max_length=150)
    bio = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to="founders/", blank=True, null=True)

    def __str__(self):
        return self.name


class StaffMember(models.Model):
    name = models.CharField(max_length=150)
    role = models.CharField(max_length=150)
    bio = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to="staff/", blank=True, null=True)

    def __str__(self):
        return self.name


class Value(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=100, blank=True, null=True)  # ex: nom d’icône FontAwesome

    def __str__(self):
        return self.title


class KeyStat(models.Model):
    label = models.CharField(max_length=150)
    value = models.PositiveIntegerField()
    icon = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.label}: {self.value}"


class Vision(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to="vision/", blank=True, null=True)

    def __str__(self):
        return self.title


class ExamResult(models.Model):
    exam_name = models.CharField(max_length=100)
    success_rate = models.PositiveIntegerField()
    total_students = models.PositiveIntegerField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.exam_name} - {self.success_rate}%"
