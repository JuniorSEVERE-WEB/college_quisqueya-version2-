# backend/core/views_dashboard.py
from django.db.models import Count
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from accounts.models import User
from academics.models import AcademicYear, Subject
from programs.models import Classroom  # <-- Classroom est dans programs
from students.models import Student     # <-- Student est dans l'app students
from professors.models import Professor # <-- Professor est dans l'app professors
from communication.models import Message, ContactMessage


# ---------------------------
#  A. STATS GLOBALES
# ---------------------------
@api_view(["GET"])
@permission_classes([IsAdminUser])
def dashboard_stats(request):
    # Étudiants / Profs (compter dans les BONNES apps)
    students_count = Student.objects.count()
    professors_count = Professor.objects.count()

    # Année académique active
    active_year = AcademicYear.objects.filter(is_active=True).values_list("name", flat=True).first()
    active_year = active_year or "—"

    # Messages non lus
    # - internes = aucune lecture (read_by M2M vide)
    unread_internal = Message.objects.filter(read_by__isnull=True).count()
    # - contacts publics non lus
    unread_contacts = ContactMessage.objects.filter(is_read=False).count()
    unread_messages_total = unread_internal + unread_contacts

    # Utilisateurs totaux et abonnés
    total_users = User.objects.count()
    abonnes_count = User.objects.filter(role="abonne").count()

    # Ratio filles/garçons (parmi les ÉLÈVES) via Student -> user.sexe
    girls_students = Student.objects.filter(user__sexe__iexact="femme").count()
    boys_students  = Student.objects.filter(user__sexe__iexact="homme").count()

    total_students_for_gender = girls_students + boys_students
    if total_students_for_gender > 0:
        girls_pct = round(girls_students * 100.0 / total_students_for_gender, 1)
        boys_pct  = round(boys_students  * 100.0 / total_students_for_gender, 1)
    else:
        girls_pct = boys_pct = 0.0

    data = {
        "students_count": students_count,
        "professors_count": professors_count,
        "active_year": active_year,
        "unread_messages": unread_messages_total,
        "total_users": total_users,
        "abonnes_count": abonnes_count,
        "gender_ratio_students": {
            "labels": ["Filles", "Garçons"],
            "data": [girls_students, boys_students],
            "percentages": {"filles": girls_pct, "garcons": boys_pct},
        },
    }
    return Response(data)


# ---------------------------
#  B. DONNÉES POUR GRAPHIQUES
# ---------------------------
@api_view(["GET"])
@permission_classes([IsAdminUser])
def dashboard_chart_data(request):
    from django.db.models.functions import TruncMonth
    from django.utils import timezone

    # 1️⃣ Élèves par classe (bar chart)
    classrooms = (
        Classroom.objects
        .annotate(total_students=Count("student"))
        .order_by("name")
    )
    students_per_class = {
        "labels": [c.name for c in classrooms],
        "data": [c.total_students for c in classrooms],
    }

    # 2️⃣ Profs par matière (doughnut)
    subjects = (
        Subject.objects
        .annotate(total_professors=Count("professors"))
        .order_by("name")
    )
    professors_per_subject = {
        "labels": [s.name for s in subjects],
        "data": [s.total_professors for s in subjects],
    }

    # 3️⃣ Répartition filles / garçons (déjà utile)
    girls_students = Student.objects.filter(user__sexe__iexact="femme").count()
    boys_students  = Student.objects.filter(user__sexe__iexact="homme").count()
    total_students_for_gender = girls_students + boys_students
    if total_students_for_gender > 0:
        girls_pct = round(girls_students * 100.0 / total_students_for_gender, 1)
        boys_pct  = round(boys_students  * 100.0 / total_students_for_gender, 1)
    else:
        girls_pct = boys_pct = 0.0

    gender_ratio = {
        "labels": ["Filles", "Garçons"],
        "data": [girls_students, boys_students],
        "percentages": {"filles": girls_pct, "garcons": boys_pct},
    }

    # 4️⃣ Abonnés par mois (NOUVEAU)
    abonnés_qs = (
        User.objects
        .filter(role="abonne", date_joined__isnull=False)
        .annotate(month=TruncMonth("date_joined"))
        .values("month")
        .annotate(count=Count("id"))
        .order_by("month")
    )

    abonne_labels = []
    abonne_data = []
    for item in abonnés_qs:
        abonne_labels.append(item["month"].strftime("%b %Y"))
        abonne_data.append(item["count"])

    abonnés_par_mois = {
        "labels": abonne_labels,
        "data": abonne_data,
    }

    return Response({
        "students_per_class": students_per_class,
        "professors_per_subject": professors_per_subject,
        "gender_ratio": gender_ratio,
        "abonnes_per_month": abonnés_par_mois,  # 👈 ajouté
    })



# ---------------------------
#  C. ACTIVITÉS RÉCENTES
# ---------------------------
@api_view(["GET"])
@permission_classes([IsAdminUser])
def dashboard_recent(request):
    # Student/Professor : on s’appuie sur user.date_joined pour la "récence"
    recent_students_qs = (
        Student.objects
        .select_related("user", "classroom")
        .order_by("-user__date_joined")[:5]
    )
    recent_professors_qs = (
        Professor.objects
        .select_related("user")
        .order_by("-user__date_joined")[:5]
    )
    recent_messages_qs = Message.objects.select_related("sender").order_by("-created_at")[:5]
    recent_contact_qs = ContactMessage.objects.order_by("-created_at")[:5]

    recent_students = [{
        "name": (s.user.get_full_name() or s.user.username),
        "classroom": getattr(s.classroom, "name", "—"),
        "date": s.user.date_joined.date().isoformat() if s.user.date_joined else None,
    } for s in recent_students_qs]

    recent_professors = [{
        "name": (p.user.get_full_name() or p.user.username),
        "date": p.user.date_joined.date().isoformat() if p.user.date_joined else None,
    } for p in recent_professors_qs]

    recent_messages = [{
        "subject": m.subject,
        "sender": (m.sender.get_full_name() or m.sender.username),
        "date": m.created_at.date().isoformat() if m.created_at else None,
    } for m in recent_messages_qs]

    recent_contacts = [{
        "subject": c.subject,
        "sender": c.name,
        "date": c.created_at.date().isoformat() if c.created_at else None,
        "is_read": c.is_read,
    } for c in recent_contact_qs]

    return Response({
        "recent_students": recent_students,
        "recent_professors": recent_professors,
        "recent_messages": recent_messages,
        "recent_contact_messages": recent_contacts,
    })
