from django.test import TestCase
from payments.forms import EnrollmentFeeForm, DonationForm
from academics.models import AcademicYear

class PaymentsFormTests(TestCase):
    def setUp(self):
        # Crée un AcademicYear pour les tests
        self.academic_year = AcademicYear.objects.create(name="2025-2026")

    def test_enrollment_fee_form_valid(self):
        """Le formulaire EnrollmentFeeForm est valide avec tous les champs requis"""
        form_data = {
            "academic_year": self.academic_year.id,  # Passe l'id de l'objet
            "amount": 1000,
        }
        form = EnrollmentFeeForm(data=form_data)
        print(form.errors)
        self.assertTrue(form.is_valid())

    def test_enrollment_fee_form_missing_fields(self):
        """Le formulaire EnrollmentFeeForm est invalide si un champ obligatoire manque"""
        form_data = {
            "amount": 1000,
        }
        form = EnrollmentFeeForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("academic_year", form.errors)

    def test_donation_form_valid(self):
        """Le formulaire DonationForm est valide avec tous les champs requis"""
        form_data = {
            "name": "Jean Dupont",
            "email": "jean@example.com",
            "amount": 500,
            "message": "Merci pour votre soutien !"
        }
        form = DonationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_donation_form_missing_fields(self):
        """Le formulaire DonationForm est valide même si le champ name est absent (car blank=True)"""
        form_data = {
            "email": "jean@example.com",
            "amount": 500,
        }
        form = DonationForm(data=form_data)
        self.assertTrue(form.is_valid())  # name n'est pas obligatoire