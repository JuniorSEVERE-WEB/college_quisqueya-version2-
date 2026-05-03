from io import BytesIO
from django.db import models
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from students.models import Student
from reports.models import Grade, SubjectCoefficient
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.units import cm
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
        total_notes += g.note * coeff
        total_coeff += coeff

    average = round(total_notes / total_coeff, 2) if total_coeff else 0

    if average >= 18:
        mention = "Excellent"
        mention_color = colors.HexColor("#4CAF50")
    elif average >= 15:
        mention = "Très bien"
        mention_color = colors.HexColor("#2196F3")
    elif average >= 12:
        mention = "Satisfaisant"
        mention_color = colors.HexColor("#FFC107")
    else:
        mention = "À améliorer"
        mention_color = colors.HexColor("#F44336")

    delivery_date = timezone.now()
    first_name = student.user.first_name
    last_name = student.user.last_name

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                            rightMargin=2*cm, leftMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('title', parent=styles['Heading1'],
                                 fontSize=16, textColor=colors.HexColor("#004080"),
                                 alignment=1, spaceAfter=6)
    subtitle_style = ParagraphStyle('subtitle', parent=styles['Normal'],
                                    fontSize=10, textColor=colors.HexColor("#666666"),
                                    alignment=1, spaceAfter=12)
    normal_style = ParagraphStyle('normal', parent=styles['Normal'], fontSize=10, spaceAfter=4)
    bold_style = ParagraphStyle('bold', parent=styles['Normal'], fontSize=10,
                                fontName='Helvetica-Bold', spaceAfter=4)

    story = []

    story.append(Paragraph("Collège Quisqueya de Léogâne", title_style))
    story.append(Paragraph("Année scolaire : 2025-2026", subtitle_style))

    header_data = [["Bulletin de Notes"]]
    header_table = Table(header_data, colWidths=[17*cm])
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#004080")),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 13),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 0.5*cm))

    info_data = [
        ["Élève :", f"{first_name} {last_name}", "Classe :", student.classroom.name],
        ["Date :", delivery_date.strftime("%d/%m/%Y"), "", ""],
    ]
    info_table = Table(info_data, colWidths=[3*cm, 6*cm, 3*cm, 5*cm])
    info_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 0.5*cm))

    grade_data = [["Matière", "Coefficient", "Note /20"]]
    for item in notes_data:
        grade_data.append([item["subject"], str(item["coefficient"]), str(item["note"])])
    grade_data.append(["Moyenne générale", str(total_coeff), f"{average}/20"])

    grade_table = Table(grade_data, colWidths=[9*cm, 4*cm, 4*cm])
    grade_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#004080")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (0, 1), (0, -1), 'LEFT'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cccccc")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.white, colors.HexColor("#f5f5f5")]),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor("#004080")),
        ('TEXTCOLOR', (0, -1), (-1, -1), colors.white),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ])
    grade_table.setStyle(grade_style)
    story.append(grade_table)
    story.append(Spacer(1, 0.5*cm))

    mention_data = [[f"Mention : {mention}"]]
    mention_table = Table(mention_data, colWidths=[17*cm])
    mention_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), mention_color),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('ROUNDEDCORNERS', [6, 6, 6, 6]),
    ]))
    story.append(mention_table)
    story.append(Spacer(1, 1.5*cm))

    sig_data = [
        ["Observation de la Direction :", "Signature des Parents :"],
        ["\n\n_____________________________", "\n\n_____________________________"],
    ]
    sig_table = Table(sig_data, colWidths=[8.5*cm, 8.5*cm])
    sig_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(sig_table)
    story.append(Spacer(1, 1*cm))

    footer_data = [[f"Remis le : {delivery_date.strftime('%d/%m/%Y')}",
                    "Collège Quisqueya de Léogâne - Tous droits réservés"]]
    footer_table = Table(footer_data, colWidths=[8.5*cm, 8.5*cm])
    footer_table.setStyle(TableStyle([
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor("#888888")),
        ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
    ]))
    story.append(footer_table)

    doc.build(story)
    pdf_bytes = buffer.getvalue()
    buffer.close()

    response = HttpResponse(pdf_bytes, content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="carnet_{first_name}_{last_name}.pdf"'
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

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                            rightMargin=2*cm, leftMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('title', parent=styles['Heading1'],
                                 fontSize=16, textColor=colors.HexColor("#004080"), alignment=1)
    story = []
    story.append(Paragraph("Collège Quisqueya - Statistiques", title_style))
    story.append(Spacer(1, 0.5*cm))

    stats_data = [
        ["Statistique", "Valeur"],
        ["Paiements total", str(payments_count)],
        ["Dons", str(donations_count)],
        ["Frais d'inscription", str(enrollment_count)],
        ["Professeurs actifs", str(active_profs_count)],
    ]
    stats_table = Table(stats_data, colWidths=[10*cm, 7*cm])
    stats_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#004080")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cccccc")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#f5f5f5")]),
        ('TOPPADDING', (0, 0), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
    ]))
    story.append(stats_table)
    story.append(Spacer(1, 0.5*cm))

    story.append(Paragraph("Élèves par année académique", ParagraphStyle(
        'section', parent=styles['Heading2'], fontSize=12,
        textColor=colors.HexColor("#004080"))))
    year_data = [["Année académique", "Nombre d'élèves"]]
    for row in students_by_year:
        year_data.append([str(row["academic_year"]), str(row["count"])])
    year_table = Table(year_data, colWidths=[10*cm, 7*cm])
    year_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#004080")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cccccc")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#f5f5f5")]),
        ('TOPPADDING', (0, 0), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
    ]))
    story.append(year_table)

    doc.build(story)
    pdf_bytes = buffer.getvalue()
    buffer.close()

    response = HttpResponse(pdf_bytes, content_type="application/pdf")
    response["Content-Disposition"] = "attachment; filename=dashboard_stats.pdf"
    return response