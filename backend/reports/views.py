from django.db import models
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from students.models import Student
from reports.models import Grade, SubjectCoefficient
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib import colors
from weasyprint import HTML, CSS
from django.template.loader import render_to_string
from django.utils import timezone

from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

from rest_framework.views import APIView
from rest_framework.response import Response
from students.models import Student
from professors.models import Professor
from payments.models import Donation, EnrollmentFee

def report_table(request):
    grades = Grade.objects.all()
    students = Student.objects.all()
    student_averages = {}
    for student in students:
        grades_student = Grade.objects.filter(student=student)
        total_notes = 0
        total_coeff = 0
        for g in grades_student:
            coeff_obj = SubjectCoefficient.objects.filter(
                subject=g.subject,
                classroom=student.classroom,
                academic_year=student.academic_year
            ).first()
            coeff = coeff_obj.coefficient if coeff_obj else 1
            total_notes += g.note
            total_coeff += coeff
        average = round(total_notes / total_coeff, 2) if total_coeff else 0
        student_averages[student.id] = average
    return render(request, "reports/report_table.html", {
        "grades": grades,
        "student_averages": student_averages,
    })

def get_subject_coefficient(subject, classroom, academic_year):
    coeff_obj = SubjectCoefficient.objects.filter(
        subject=subject,
        classroom=classroom,
        academic_year=academic_year
    ).first()
    return coeff_obj.coefficient if coeff_obj else 1

def student_report_pdf(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    grades = Grade.objects.filter(student=student).order_by('subject__name')

    notes_data = []
    total_notes = 0
    total_coeff = 0
    for g in grades:
        coeff = get_subject_coefficient(g.subject, student.classroom, student.academic_year)
        notes_data.append({
            "subject": g.subject.name,
            "note": g.note,
            "coefficient": coeff
        })
        total_notes += g.note
        total_coeff += coeff

    average = round((total_notes / total_coeff) * 100, 2) if total_coeff else 0

    if average >= 90:
        mention = "Excellent"
        badge_color = "#4CAF50"
    elif average >= 75:
        mention = "Très bien"
        badge_color = "#2196F3"
    elif average >= 60:
        mention = "Satisfaisant"
        badge_color = "#FFC107"
    else:
        mention = "À améliorer"
        badge_color = "#F44336"

    delivery_date = timezone.now()
    step = getattr(student, "step", getattr(student.classroom, "step", ""))
    trimester = getattr(student, "trimester", getattr(student.classroom, "trimester", ""))

    html_string = render_to_string("reports/student_report_web.html", {
        "student": student,
        "notes_data": notes_data,
        "average": average,
        "total_coeff": total_coeff,
        "mention": mention,
        "badge_color": badge_color,
        "school_logo": "/static/img/logo.png",
        "school_name": "Collège Quisqueya",
        "school_year": "2025-2026",
        "classroom": student.classroom.name,
        "delivery_date": delivery_date,
        "step": step,
        "trimester": trimester,
    })

    pdf_file = HTML(string=html_string).write_pdf()
    response = HttpResponse(pdf_file, content_type="application/pdf")
    response["Content-Disposition"] = f"attachment; filename=student_{student.id}_report.pdf"
    return response

class DashboardStatsAPIView(APIView):
    def get(self, request):
        students_by_year = (
            Student.objects.values("academic_year")
            .annotate(count=models.Count("id"))
            .order_by("academic_year")
        )
        donations_count = Donation.objects.count()
        enrollment_count = EnrollmentFee.objects.count()
        payments_count = donations_count + enrollment_count
        active_profs_count = Professor.objects.filter(user__is_active=True).count()

        return Response({
            "students_by_year": list(students_by_year),
            "payments_count": payments_count,
            "donations_count": donations_count,
            "enrollment_count": enrollment_count,
            "active_profs_count": active_profs_count,
        })

def dashboard_view(request):
    students_by_year = (
        Student.objects.values("academic_year")
        .annotate(count=models.Count("id"))
        .order_by("academic_year")
    )
    donations_count = Donation.objects.count()
    enrollment_count = EnrollmentFee.objects.count()
    payments_count = donations_count + enrollment_count
    active_profs_count = Professor.objects.filter(user__is_active=True).count()

    return render(request, "reports/dashboard.html", {
        "students_by_year": students_by_year,
        "payments_count": payments_count,
        "donations_count": donations_count,
        "enrollment_count": enrollment_count,
        "active_profs_count": active_profs_count,
    })

def dashboard_pdf_view(request):
    students_by_year = (
        Student.objects.values("academic_year")
        .annotate(count=models.Count("id"))
        .order_by("academic_year")
    )
    donations_count = Donation.objects.count()
    enrollment_count = EnrollmentFee.objects.count()
    payments_count = donations_count + enrollment_count
    active_profs_count = Professor.objects.filter(user__is_active=True).count()

    html_string = render_to_string("reports/dashboard_pdf.html", {
        "students_by_year": students_by_year,
        "payments_count": payments_count,
        "donations_count": donations_count,
        "enrollment_count": enrollment_count,
        "active_profs_count": active_profs_count,
    })

    pdf_file = HTML(string=html_string).write_pdf()
    response = HttpResponse(pdf_file, content_type="application/pdf")
    response["Content-Disposition"] = "attachment; filename=dashboard_stats.pdf"
    return response