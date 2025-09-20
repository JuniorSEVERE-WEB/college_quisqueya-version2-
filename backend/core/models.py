from django.db import models
from django.conf import settings
from .utils.current import get_current_user

class AuditModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True, blank=True, on_delete=models.SET_NULL,
        related_name="created_%(class)ss", editable=False
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True, blank=True, on_delete=models.SET_NULL,
        related_name="updated_%(class)ss", editable=False
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        user = get_current_user()
        if user and not getattr(user, "is_anonymous", True):
            if not self.pk and not self.created_by_id:
                self.created_by = user
            self.updated_by = user
        super().save(*args, **kwargs)