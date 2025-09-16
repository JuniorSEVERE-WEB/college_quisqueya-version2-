import pytest
from academics.models import AcademicYear, Trimester, Step, Classroom, Subject, Student, Note

@pytest.mark.django_db
def test_student_moyenne_etape_and_annuelle():
    year = AcademicYear.objects.create(name="2025-2026", is_active=True)
    trimester = Trimester.objects.create(name="Trimestre 1", academic_year=year)
    step = Step.objects.create(name="Étape 1", trimester=trimester, is_active=True)
    classroom = Classroom.objects.create(name="6ème A", academic_year=year)
    subject1 = Subject.objects.create(name="Math", classroom=classroom, coefficient=2)
    subject2 = Subject.objects.create(name="Français", classroom=classroom, coefficient=1)
    student = Student.objects.create(user_id=1, classroom=classroom)
    Note.objects.create(student=student, subject=subject1, step=step, value=15)
    Note.objects.create(student=student, subject=subject2, step=step, value=10)
    assert student.moyenne_etape(step) == pytest.approx((15*2 + 10*1)/3)
    assert student.moyenne_annuelle() == pytest.approx((15*2 + 10*1)/3)