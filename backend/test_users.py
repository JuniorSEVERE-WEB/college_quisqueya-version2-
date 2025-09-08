from django.contrib.auth import get_user_model
from professors.models import Professor
from employees.models import Employee

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

print("\n==== Test inscription Professor ====")
User.objects.filter(username="test_professor").delete()
p = User.objects.create_user(
    username="test_professor",
    email="test_professor@test.ht",
    password="12345",
    role="professor"
)
print(f"Professor créé → is_active={p.is_active}")  # doit être False

# Création du profil Professor lié à l'utilisateur
professor_profile = Professor.objects.create(
    user=p,
    academic_year_id=1,  # à adapter selon l'ID existant
    program_id=1,        # à adapter selon l'ID existant
    subjects="Maths, Physique",
)
professor_profile.classrooms.set([])  # à adapter si tu veux lier des classes

print(f"Profil Professor créé → user={professor_profile.user.username}, subjects={professor_profile.subjects}")

print("\n==== Test inscription Employee ====")
User.objects.filter(username="test_employee").delete()
e = User.objects.create_user(
    username="test_employee",
    email="test_employee@test.ht",
    password="12345",
    role="employee"
)
print(f"Employee créé → is_active={e.is_active}")  # doit être False

# Création du profil Employee lié à l'utilisateur
employee_profile = Employee.objects.create(
    user=e,
    academic_year_id=1,  # à adapter selon l'ID existant
    position="Secrétaire",
    hire_date="2025-09-08",
    department="Administration"
)
print(f"Profil Employee créé → user={employee_profile.user.username}, position={employee_profile.position}")

print("\n==== Test activation manuelle ====")
u.is_active = True
u.save()
print(f"Student activé par admin → is_active={u.is_active} (email envoyé si EMAIL_BACKEND=console)")

p.is_active = True
p.save()
print(f"Professor activé par admin → is_active={p.is_active} (email envoyé si EMAIL_BACKEND=console)")

e.is_active = True
e.save()
print(f"Employee activé par admin → is_active={e.is_active} (email envoyé si EMAIL_BACKEND=console)")