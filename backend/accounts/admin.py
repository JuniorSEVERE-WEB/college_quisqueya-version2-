from django.contrib import admin
from django.contrib.auth import get_user_model
from .utils import send_activation_email

User = get_user_model()

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "role", "is_active")
    list_filter = ("role", "is_active")
    actions = ["activer_comptes"]

    @admin.action(description="Valider les comptes sélectionnés")
    def activer_comptes(self, request, queryset):
        for user in queryset:
            if not user.is_active:
                user.is_active = True
                user.save()
                send_activation_email(user)  # 📧 envoi email

        self.message_user(
            request,
            f"{queryset.count()} compte(s) validé(s) et email(s) envoyé(s). ✅"
        )
