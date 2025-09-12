from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from payments.models import EnrollmentFee, Donation, Transaction

User = get_user_model()

class PaymentsViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="student", password="pass", email="student@test.ht")

    def test_pay_enrollment_fee_get(self):
        self.client.login(username="student", password="pass")
        response = self.client.get(reverse("payments:pay_enrollment_fee"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "payments/pay_enrollment_fee.html")

    def test_pay_enrollment_fee_post(self):
        self.client.login(username="student", password="pass")
        form_data = {
            "academic_year": 1,  # adapte selon ton modèle
            "amount": 1000,
        }
        # Crée un AcademicYear si nécessaire
        from academics.models import AcademicYear
        year = AcademicYear.objects.create(name="2025-2026")
        form_data["academic_year"] = year.id

        response = self.client.post(reverse("payments:pay_enrollment_fee"), data=form_data)
        self.assertRedirects(response, reverse("payments:payment_success"))
        self.assertTrue(EnrollmentFee.objects.filter(student=self.user, academic_year=year).exists())
        self.assertTrue(Transaction.objects.filter(user=self.user, payment_type="enrollment").exists())

    def test_make_donation_get(self):
        response = self.client.get(reverse("payments:make_donation"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "payments/make_donation.html")

    def test_make_donation_post(self):
        form_data = {
            "name": "Jean",
            "email": "jean@test.ht",
            "amount": 500,
            "message": "Bravo !"
        }
        response = self.client.post(reverse("payments:make_donation"), data=form_data)
        self.assertRedirects(response, reverse("payments:payment_success"))
        self.assertTrue(Donation.objects.filter(email="jean@test.ht").exists())
        self.assertTrue(Transaction.objects.filter(payment_type="donation").exists())

    def test_payment_success_view(self):
        response = self.client.get(reverse("payments:payment_success"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "payments/payment_success.html")