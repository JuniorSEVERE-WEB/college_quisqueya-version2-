from django.contrib.auth import get_user_model
from professors.models import Professor
from employees.models import Employee
from alumni.models import Alumni
from academics.models import AcademicYear
from programs.models import Program

User = get_user_model()

# Vérifie ou crée l'année académique et le programme
academic_year, _ = AcademicYear.objects.get_or_create(id=1, defaults={"name": "2025-2026"})
program, _ = Program.objects.get_or_create(id=1, defaults={"name": "Primaire"})

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
    academic_year=academic_year,
    program=program,
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
    academic_year=academic_year,
    position="Secrétaire",
    hire_date="2025-09-08",
    department="Administration"
)
print(f"Profil Employee créé → user={employee_profile.user.username}, position={employee_profile.position}")

print("\n==== Test inscription Alumni ====")
User.objects.filter(username="test_alumni").delete()
a = User.objects.create_user(
    username="test_alumni",
    email="test_alumni@test.ht",
    password="12345",
    role="alumni"
)
print(f"Alumni créé → is_active={a.is_active}")  # doit être False ou selon ta logique

# Création du profil Alumni lié à l'utilisateur
alumni_profile = Alumni.objects.create(
    user=a,
    role="student",  # ou "professor", "employee"
    year_left=2025,
    promo_name="Promo Excellence",
    years_interval="2020-2025",
    # proof_document peut être laissé vide pour le test
)
print(f"Profil Alumni créé → user={alumni_profile.user.username}, promo={alumni_profile.promo_name}")

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

a.is_active = True
a.save()
print(f"Alumni activé par admin → is_active={a.is_active} (email envoyé si EMAIL_BACKEND=console)")