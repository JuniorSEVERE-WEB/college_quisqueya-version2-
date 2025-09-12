from django.db import models 
from django.core.exceptions import ValidationError
from accounts.models import User

# --- Validateur personnalisé pour la taille des images ---
def validate_image_size(image):
    max_size = 3 * 1024 * 1024  # 3 MB en bytes
    if image.size > max_size:
        raise ValidationError("L’image ne doit pas dépasser 3 MB.")
    

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
        

class Article(models.Model):
    VISIBILITY_CHOICES = [
        ("all", "Tout le monde"),            # visiteurs inclus
        ("students", "Étudiants"),
        ("professors", "Professeurs"),
        ("employees", "Employés"),
        ("alumni", "Alumni"),
        ("custom", "Groupe personnalisé"),  # ex: combiner certains rôles
    ]

    title = models.CharField(max_length=200)
    image = models.ImageField(
        upload_to="blog_images/",
        validators=[validate_image_size]  
    )
    description = models.TextField()
    date_published = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True)
    visibility = models.CharField(
        max_length=20,
        choices=VISIBILITY_CHOICES,
        default="all"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    tags = models.ManyToManyField(Tag, related_name="articles", blank=True)


    def __str__(self):
        return self.title
    
    @property
    def likes_count(self):
        return self.reactions.filter(reaction_type=Reaction.LIKE).count()

    @property
    def dislikes_count(self):
        return self.reactions.filter(reaction_type=Reaction.DISLIKE).count()


class Comment(models.Model):
    article = models.ForeignKey(
        Article, 
        on_delete=models.CASCADE, 
        related_name="comments"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = models.ForeignKey(
        "self", 
        null=True, 
        blank=True, 
        on_delete=models.CASCADE, 
        related_name="replies"
    )
    text = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.text[:30]}"
    
    @property
    def likes_count(self):
        return self.reactions.filter(reaction_type=Reaction.LIKE).count()

    @property
    def dislikes_count(self):
        return self.reactions.filter(reaction_type=Reaction.DISLIKE).count()


class Reaction(models.Model):
    LIKE = "like"
    DISLIKE = "dislike"
    REACTION_CHOICES = [
        (LIKE, "Like"),
        (DISLIKE, "Dislike"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(
        Article, 
        related_name="reactions", 
        null=True, blank=True, 
        on_delete=models.CASCADE
    )
    comment = models.ForeignKey(
        Comment, 
        related_name="reactions", 
        null=True, blank=True, 
        on_delete=models.CASCADE
    )
    reaction_type = models.CharField(max_length=10, choices=REACTION_CHOICES)

    class Meta:
        unique_together = ("user", "article", "comment")  # un seul like/dislike par user

    def __str__(self):
        target = self.article.title if self.article else f"Comment {self.comment.id}"
        return f"{self.user.username} - {self.reaction_type} on {target}"
