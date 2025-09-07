from django.contrib.auth import get_user_model

User = get_user_model()


print("==== Test inscription Student ====")
User.objects.filter(username="test_student").delete()
u = User.objects.create_user(
    username="test_student",
    email="test_student@test.ht",
    password="12345",
    role="student"
)
print(f"Student créé → is_active={u.is_active}")  # doit être False


print("\n==== Test inscription Membersite ====")
User.objects.filter(username="test_member").delete()
m = User.objects.create_user(
    username="test_member",
    email="test_member@test.ht",
    password="12345",
    role="membersite"
)
print(f"Membersite créé → is_active={m.is_active}")  # doit être True

print("\n==== Test activation manuelle ====")
u.is_active = True
u.save()
print(f"Student activé par admin → is_active={u.is_active} (email envoyé si EMAIL_BACKEND=console)")
