from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.shortcuts import render
from students.models import Student
from reports.models import Grade, SubjectCoefficient
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib import colors
from weasyprint import HTML, CSS
from django.template.loader import render_to_string

from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def report_table(request):
    grades = Grade.objects.all()
    return render(request, "reports/report_table.html", {"grades": grades})

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

    # Préparer les notes et coefficients pour le template
    notes_data = []
    total_score = 0
    total_coeff = 0
    for g in grades:
        coeff = get_subject_coefficient(g.subject, student.classroom, student.academic_year)
        notes_data.append({
            "subject": g.subject.name,
            "note": g.note,
            "coefficient": coeff
        })
        total_score += g.note * coeff
        total_coeff += coeff

    average = round(total_score / total_coeff, 2) if total_coeff else 0

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

    html_string = render_to_string("reports/student_report_web.html", {
        "student": student,
        "notes_data": notes_data,
        "average": average,
        "mention": mention,
        "badge_color": badge_color,
        "school_logo": "/static/img/logo.png",
        "school_name": "Collège Quisqueya",
        "school_year": "2025-2026",
        "classroom": student.classroom.name
    })

    pdf_file = HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf()

    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'filename=Bulletin_{student.first_name}_{student.last_name}.pdf'
    return response