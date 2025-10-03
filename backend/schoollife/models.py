from django.db import models
from django.core.exceptions import ValidationError

# --- Validateur personnalisé pour limiter la taille des images ---
def validate_image_size(image):
    max_size = 3 * 1024 * 1024  # 3 MB
    if image.size > max_size:
        raise ValidationError("L’image ne doit pas dépasser 3 MB.")

class Club(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    photo = models.ImageField(   # ✅ ajout photo
        upload_to="clubs/",
        blank=True,
        null=True,
        validators=[validate_image_size]
    )

    def __str__(self):
        return self.name


class Event(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name="events")
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    logo = models.ImageField(   # ✅ ajout logo
        upload_to="events/",
        blank=True,
        null=True,
        validators=[validate_image_size]
    )

    def __str__(self):
        return f"{self.title} ({self.date})"


class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100, blank=True, null=True)
    message = models.TextField()
    photo = models.ImageField(
        upload_to="testimonials/",
        blank=True,
        null=True,
        validators=[validate_image_size]
    )

    def __str__(self):
        return f"Témoignage de {self.name}"


class GalleryItem(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(
        upload_to="gallery/",
        validators=[validate_image_size]
    )
    date_added = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.title
