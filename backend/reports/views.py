from django.shortcuts import render, get_object_or_404
from programs.models import Classroom, Subject
from students.models import Student
from .models import Grade, SubjectCoefficient, ReportSession

def report_table(request, classroom_id, session_id):
    classroom = get_object_or_404(Classroom, id=classroom_id)
    session = get_object_or_404(ReportSession, id=session_id)

    # 1. Récupérer toutes les matières de la classe
    subjects = Subject.objects.filter(classroom=classroom)

    # 2. Récupérer tous les étudiants de la classe
    students = Student.objects.filter(classroom=classroom)

    # 3. Récupérer les coefficients des matières
    coefficients = {
        subj.id: SubjectCoefficient.objects.filter(subject=subj).first().coefficient
        if SubjectCoefficient.objects.filter(subject=subj).exists()
        else 1
        for subj in subjects
    }

    # 4. Construire les lignes (notes de chaque élève)
    table = []
    for student in students:
        scores = {}
        total_points = 0
        total_coeffs = 0

        for subj in subjects:
            grade = Grade.objects.filter(student=student, subject=subj, report_session=session).first()
            note = grade.note if grade else None
            if note is not None:
                scores[subj.id] = note
                total_points += note
                total_coeffs += coefficients[subj.id]

        # moyenne pondérée
        average = round((total_points / total_coeffs) * 100, 2) if total_coeffs > 0 else 0

        table.append({
            "student": student,
            "scores": scores,
            "average": average,
        })

    # 5. Moyennes par matière (colonnes)
    subject_averages = {}
    for subj in subjects:
        notes = Grade.objects.filter(subject=subj, report_session=session, student__in=students).values_list("note", flat=True)
        subject_averages[subj.id] = round(sum(notes) / len(notes), 2) if notes else 0

    # 6. Moyenne de la classe
    class_avg = round(sum(row["average"] for row in table) / len(table), 2) if table else 0

    context = {
        "classroom": classroom,
        "report_session": session,
        "subjects": subjects,
        "coefficients": coefficients,
        "table": table,
        "subject_averages": subject_averages,
        "class_avg": class_avg,
    }

    return render(request, "reports/report_table.html", context)
