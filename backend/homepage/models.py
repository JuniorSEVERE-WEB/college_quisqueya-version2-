from django.db import models


class Slide(models.Model):
    image = models.ImageField(upload_to="homepage/slides/")
    text = models.CharField(max_length=255)

    def __str__(self):
        return f"Slide: {self.text[:30]}..."


class SlideTitle(models.Model):
    slide = models.ForeignKey(Slide, related_name="titles", on_delete=models.CASCADE)
    title = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.title} (Slide {self.slide.id})"


class Welcome(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        return self.title


class Value(models.Model):
    icon = models.CharField(max_length=10, help_text="Emoji ou petit symbole")
    title = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.title
