from django.db import models

class Club(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class Event(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name="events")
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()

    def __str__(self):
        return f"{self.title} ({self.date})"


class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100, blank=True, null=True)
    message = models.TextField()
    photo = models.ImageField(upload_to="testimonials/", blank=True, null=True)

    def __str__(self):
        return f"Témoignage de {self.name}"


class GalleryItem(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to="gallery/")
    date_added = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.title
