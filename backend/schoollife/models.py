# schoollife/models.py
from django.db import models

class Club(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name="events", default=1)  # ✅ Ajout

    def __str__(self):
        return self.title
