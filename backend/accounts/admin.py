from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

User = get_user_model()

# Utilise les formulaires dédiés s’ils existent, sinon fallback local
try:
    from .forms import AdminUserCreationForm, AdminUserChangeForm  # si définis dans accounts/forms.py
except Exception:
    class AdminUserCreationForm(UserCreationForm):
        class Meta(UserCreationForm.Meta):
            model = User
            fields = ("username", "email", "first_name", "last_name")

    class AdminUserChangeForm(UserChangeForm):
        class Meta(UserChangeForm.Meta):
            model = User
            fields = (
                "username", "email", "first_name", "last_name",
                "is_active", "is_staff", "is_superuser", "groups", "user_permissions"
            )

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    add_form = AdminUserCreationForm
    form = AdminUserChangeForm
    model = User

    list_display = ("username", "email", "is_active", "is_staff", "is_superuser")
    list_filter = ("is_active", "is_staff", "is_superuser", "groups")
    search_fields = ("username", "email", "first_name", "last_name")
    ordering = ("username",)

    fieldsets = (
        (_("Identifiants"), {"fields": ("username", "password")}),
        (_("Informations personnelles"), {"fields": ("first_name", "last_name", "email", "photo")}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        (_("Dates importantes"), {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (_("Création d’utilisateur"), {
            "classes": ("wide",),
            "fields": ("username", "email", "first_name", "last_name", "photo", "password1", "password2"),
        }),
    )

    actions = ["activer_comptes"]

    @admin.action(description="Valider les comptes sélectionnés")
    def activer_comptes(self, request, queryset):
        count = 0
        for user in queryset:
            if not user.is_active:
                user.is_active = True
                user.save(update_fields=["is_active"])
                try:
                    from .utils import send_activation_email
                    send_activation_email(user)
                except Exception:
                    pass
                count += 1
        self.message_user(request, f"{count} compte(s) validé(s). ✅")