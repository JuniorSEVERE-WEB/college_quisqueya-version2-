# accounts/test_signal.py
import os
import django

# ⚠️ Adapter au nom de ton projet Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

def run_test():
    # On prend le premier utilisateur existant (adapte si besoin)
    user, created = User.objects.get_or_create(
        username="testuser",
        defaults={"email": "test@example.com", "password": "password123"}
    )

    if created:
        print("✅ Utilisateur créé avec succès.")
    else:
        print("ℹ️ Utilisateur déjà existant.")

    # Simuler une activation
    print(f"Avant activation: is_active={user.is_active}")
    user.is_active = True
    user.save()
    print(f"Après activation: is_active={user.is_active}")

if __name__ == "__main__":
    run_test()
