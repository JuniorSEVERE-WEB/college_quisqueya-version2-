# backend/core/views_dashboard.py
from django.db.models import Count, Q
from django.db.models.functions import TruncMonth
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from django.utils import timezone

# Import des modèles
from accounts.models import User
from academics.models import AcademicYear, Subject
from programs.models import Classroom
from students.models import Student
from professors.models import Professor
from communication.models import Message, ContactMessage
from blog.models import Article, Comment, Reaction
from payments.models import Donation


# ============================================================
# A. STATS GLOBALES
# ============================================================
@api_view(["GET"])
@permission_classes([IsAdminUser])
def dashboard_stats(request):
    """Statistiques globales principales pour le dashboard"""

    # Comptages basiques
    students_count = Student.objects.count()
    professors_count = Professor.objects.count()
    employees_count = User.objects.filter(role="employee").count() if hasattr(User, "role") else 0
    programs_count = Classroom.objects.count()
    messages_count = Message.objects.count()
    articles_count = Article.objects.count()
    comments_count = Comment.objects.count()
    donations_count = Donation.objects.count()

    # Likes / Unlikes à partir du modèle Reaction
    likes_count = Reaction.objects.filter(reaction_type=Reaction.LIKE).count()
    unlikes_count = Reaction.objects.filter(reaction_type=Reaction.DISLIKE).count()

    # Utilisateurs et abonnés
    total_users = User.objects.count()
    abonnes_count = User.objects.filter(role="abonne").count()

    # Année académique active
    active_year = AcademicYear.objects.filter(is_active=True).values_list("name", flat=True).first() or "—"

    # Messages non lus
    unread_internal = Message.objects.filter(read_by__isnull=True).count()
    unread_contacts = ContactMessage.objects.filter(is_read=False).count()
    unread_messages_total = unread_internal + unread_contacts

    # Ratio Hommes / Femmes (tous utilisateurs)
    total_males = User.objects.filter(sexe__iexact="homme").count()
    total_females = User.objects.filter(sexe__iexact="femme").count()
    gender_total = total_males + total_females or 1
    male_pct = round((total_males / gender_total) * 100, 1)
    female_pct = round((total_females / gender_total) * 100, 1)

    data = {
        "students_count": students_count,
        "professors_count": professors_count,
        "employees_count": employees_count,
        "programs_count": programs_count,
        "messages_count": messages_count,
        "articles_count": articles_count,
        "comments_count": comments_count,
        "donations_count": donations_count,
        "likes_count": likes_count,
        "unlikes_count": unlikes_count,
        "abonnes_count": abonnes_count,
        "total_users": total_users,
        "unread_messages": unread_messages_total,
        "active_year": active_year,
        "gender_ratio": {
            "labels": ["Hommes", "Femmes"],
            "data": [total_males, total_females],
            "percentages": {"hommes": male_pct, "femmes": female_pct},
        },
    }
    return Response(data)


# ============================================================
# B. DONNÉES POUR GRAPHIQUES
# ============================================================
@api_view(["GET"])
@permission_classes([IsAdminUser])
def dashboard_chart_data(request):
    """Graphiques du dashboard (élèves, profs, abonnés, etc.)"""

    # 1️⃣ Élèves par classe
    classrooms = (
        Classroom.objects
        .annotate(total_students=Count("student"))
        .order_by("name")
    )
    students_per_class = {
        "labels": [c.name for c in classrooms],
        "data": [c.total_students for c in classrooms],
    }

    # 2️⃣ Professeurs par matière
    subjects = (
        Subject.objects
        .annotate(total_professors=Count("professors"))
        .order_by("name")
    )
    professors_per_subject = {
        "labels": [s.name for s in subjects],
        "data": [s.total_professors for s in subjects],
    }

    # 3️⃣ Ratio filles / garçons parmi les élèves
    girls_students = Student.objects.filter(user__sexe__iexact="femme").count()
    boys_students = Student.objects.filter(user__sexe__iexact="homme").count()
    total_students = girls_students + boys_students or 1
    girls_pct = round(girls_students * 100.0 / total_students, 1)
    boys_pct = round(boys_students * 100.0 / total_students, 1)
    gender_ratio_students = {
        "labels": ["Filles", "Garçons"],
        "data": [girls_students, boys_students],
        "percentages": {"filles": girls_pct, "garcons": boys_pct},
    }

    # 4️⃣ Abonnés par mois
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
        if item["month"]:
            abonne_labels.append(item["month"].strftime("%b %Y"))
            abonne_data.append(item["count"])

    abonnés_par_mois = {"labels": abonne_labels, "data": abonne_data}

    return Response({
        "students_per_class": students_per_class,
        "professors_per_subject": professors_per_subject,
        "gender_ratio_students": gender_ratio_students,
        "abonnes_per_month": abonnés_par_mois,
    })


# ============================================================
# C. ACTIVITÉS RÉCENTES
# ============================================================
@api_view(["GET"])
@permission_classes([IsAdminUser])
def dashboard_recent(request):
    """Liste des activités récentes (élèves, profs, messages, etc.)"""

    recent_students_qs = (
        Student.objects.select_related("user", "classroom")
        .order_by("-user__date_joined")[:5]
    )
    recent_professors_qs = (
        Professor.objects.select_related("user")
        .order_by("-user__date_joined")[:5]
    )
    recent_messages_qs = Message.objects.select_related("sender").order_by("-created_at")[:5]
    recent_contact_qs = ContactMessage.objects.order_by("-created_at")[:5]

    recent_students = [
        {
            "name": s.user.get_full_name() or s.user.username,
            "classroom": getattr(s.classroom, "name", "—"),
            "date": s.user.date_joined.date().isoformat() if s.user.date_joined else None,
        }
        for s in recent_students_qs
    ]
    recent_professors = [
        {
            "name": p.user.get_full_name() or p.user.username,
            "date": p.user.date_joined.date().isoformat() if p.user.date_joined else None,
        }
        for p in recent_professors_qs
    ]
    recent_messages = [
        {
            "subject": m.subject,
            "sender": m.sender.get_full_name() or m.sender.username,
            "date": m.created_at.date().isoformat() if m.created_at else None,
        }
        for m in recent_messages_qs
    ]
    recent_contacts = [
        {
            "subject": c.subject,
            "sender": c.name,
            "date": c.created_at.date().isoformat() if c.created_at else None,
            "is_read": c.is_read,
        }
        for c in recent_contact_qs
    ]

    return Response({
        "recent_students": recent_students,
        "recent_professors": recent_professors,
        "recent_messages": recent_messages,
        "recent_contact_messages": recent_contacts,
    })
