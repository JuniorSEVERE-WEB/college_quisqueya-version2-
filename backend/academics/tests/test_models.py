import pytest
from django.core.exceptions import ValidationError
from academics.models import AcademicYear, Trimester, Step, Classroom


@pytest.mark.django_db
def test_academic_year_creates_trimesters():
    year = AcademicYear.objects.create(name="2025-2026", is_active=True)
    trimesters = year.trimesters.all()
    assert trimesters.count() == 3
    assert [t.name for t in trimesters] == ["Trimestre 1", "Trimestre 2", "Trimestre 3"]


@pytest.mark.django_db
def test_trimester_str():
    year = AcademicYear.objects.create(name="2025-2026")
    trimester = Trimester.objects.create(name="Trimestre 1", academic_year=year)
    assert str(trimester) == "Trimestre 1 (2025-2026)"


@pytest.mark.django_db
def test_step_constraints():
    year = AcademicYear.objects.create(name="2025-2026")
    trimester = year.trimesters.first()

    # Ajoute deux étapes valides
    Step.objects.create(name="Étape 1", trimester=trimester, is_active=True)
    Step.objects.create(name="Étape 2", trimester=trimester)

    # La troisième doit échouer
    with pytest.raises(ValidationError):
        Step(name="Étape 3", trimester=trimester).save()


@pytest.mark.django_db
def test_classroom_unique_name_per_year():
    year = AcademicYear.objects.create(name="2025-2026")
    Classroom.objects.create(name="6ème A", capacity=30, academic_year=year)

    # Même nom dans la même année → erreur
    with pytest.raises(Exception):
        Classroom.objects.create(name="6ème A", capacity=25, academic_year=year)


@pytest.mark.django_db
def test_step_min_and_max_constraints():
    year = AcademicYear.objects.create(name="2025-2026")
    trimesters = year.trimesters.all()

    # Crée 3 étapes valides (min atteint)
    Step.objects.create(name="Étape 1", trimester=trimesters[0], is_active=True)
    Step.objects.create(name="Étape 2", trimester=trimesters[1])
    Step.objects.create(name="Étape 3", trimester=trimesters[2])

    # Ajoute 2 autres étapes (max atteint = 5)
    Step.objects.create(name="Étape 4", trimester=trimesters[0])
    Step.objects.create(name="Étape 5", trimester=trimesters[1])

    # La 6ème doit échouer
    with pytest.raises(ValidationError):
        Step(name="Étape 6", trimester=trimesters[2]).clean()


@pytest.mark.django_db
def test_only_one_active_step_per_year():
    year = AcademicYear.objects.create(name="2025-2026")
    trimesters = year.trimesters.all()

    step1 = Step.objects.create(name="Étape 1", trimester=trimesters[0], is_active=True)
    step2 = Step.objects.create(name="Étape 2", trimester=trimesters[1], is_active=True)

    step1.refresh_from_db()
    step2.refresh_from_db()

    # step2 devient active → step1 doit être désactivée
    assert not step1.is_active
    assert step2.is_active


@pytest.mark.django_db
def test_cannot_disable_all_steps():
    year = AcademicYear.objects.create(name="2025-2026")
    trimester = year.trimesters.first()

    step = Step.objects.create(name="Étape 1", trimester=trimester, is_active=True)

    # Essaye de désactiver la seule étape active
    step.is_active = False
    with pytest.raises(ValidationError):
        step.save()
