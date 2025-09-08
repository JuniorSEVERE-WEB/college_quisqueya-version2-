import os
import sys
import django

# Ajout du chemin pour que Python trouve le module backend
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

def run_test():
    user, created = User.objects.get_or_create(
        username="testuser",
        defaults={
            "email": "test@example.com",
            "password": "password123",
            "is_active": False   # 🔹 Créé inactif
        }
    )

    if created:
        print("✅ Utilisateur créé avec succès (inactif).")
    else:
        print("ℹ️ Utilisateur déjà existant.")

    print(f"Avant activation: is_active={user.is_active}")
    # Simuler activation
    user.is_active = True
    user.save()
    print(f"Après activation: is_active={user.is_active}")

if __name__ == "__main__":
    run_test()
