from django.db import models
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# Import des modèles
from academics.models import AcademicYear
from students.models import Student
from professors.models import Professor
from employees.models import Employee
from payments.models import EnrollmentFee, Donation
from communication.models import ContactMessage
from alumni.models import Alumni
from blog.models import Article, Comment


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    """
    Retourne les statistiques principales du dashboard
    pour l'année académique active.
    """

    # 1️⃣ Année académique active
    academic_year = AcademicYear.objects.filter(is_active=True).first()
    if not academic_year:
        return Response({"error": "Aucune année académique active trouvée."}, status=404)

    # 2️⃣ QuerySets
    students_qs = Student.objects.filter(academic_year=academic_year)
    professors_qs = Professor.objects.filter(academic_year=academic_year)
    employees_qs = Employee.objects.filter(academic_year=academic_year)
    payments_qs = EnrollmentFee.objects.filter(academic_year=academic_year, is_confirmed=True)
    donations_qs = Donation.objects.all()
    messages_qs = ContactMessage.objects.all()
    alumni_qs = Alumni.objects.all()
    articles_qs = Article.objects.all()
    comments_qs = Comment.objects.all()

    # 3️⃣ Comptage manuel des sexes (parcourir les relations OneToOne)
    def count_by_sex(queryset):
        male = 0
        female = 0
        for obj in queryset.select_related("user"):
            if hasattr(obj.user, "sex"):
                if obj.user.sex == "M":
                    male += 1
                elif obj.user.sex == "F":
                    female += 1
        return male, female

    students_male, students_female = count_by_sex(students_qs)
    professors_male, professors_female = count_by_sex(professors_qs)
    employees_male, employees_female = count_by_sex(employees_qs)

    # 4️⃣ Données finales
    data = {
        "academic_year": academic_year.name,
        "students_total": students_qs.count(),
        "professors_total": professors_qs.count(),
        "employees_total": employees_qs.count(),
        "payments_total": payments_qs.aggregate(total=models.Sum("amount"))["total"] or 0,
        "donations_total": donations_qs.aggregate(total=models.Sum("amount"))["total"] or 0,
        "messages_total": messages_qs.count(),
        "alumni_total": alumni_qs.count(),
        "articles_total": articles_qs.count(),
        "comments_total": comments_qs.count(),
        # ✅ Répartition par sexe (fiable)
        "students_male": students_male,
        "students_female": students_female,
        "professors_male": professors_male,
        "professors_female": professors_female,
        "employees_male": employees_male,
        "employees_female": employees_female,
    }

    return Response(data)
