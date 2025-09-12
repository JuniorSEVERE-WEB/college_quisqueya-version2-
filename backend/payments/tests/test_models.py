from django.test import TestCase
from django.contrib.auth import get_user_model
from academics.models import AcademicYear
from payments.models import EnrollmentFee, Donation, Transaction

User = get_user_model()

class PaymentsModelsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="student", password="pass", email="student@test.ht")
        self.academic_year = AcademicYear.objects.create(name="2025-2026")

    def test_enrollment_fee_creation(self):
        fee = EnrollmentFee.objects.create(
            student=self.user,
            academic_year=self.academic_year,
            amount=1500.00
        )
        self.assertEqual(str(fee), f"Frais {self.user} - {self.academic_year} - {fee.amount} Gdes")
        self.assertFalse(fee.is_confirmed)

    def test_donation_creation(self):
        donation = Donation.objects.create(
            donor=self.user,
            name="Jean",
            email="jean@test.ht",
            amount=500.00,
            message="Bravo !"
        )
        self.assertEqual(str(donation), f"Don Jean - 500.0 Gdes")
        self.assertEqual(donation.donor, self.user)

    def test_transaction_creation(self):
        fee = EnrollmentFee.objects.create(
            student=self.user,
            academic_year=self.academic_year,
            amount=2000.00
        )
        transaction = Transaction.objects.create(
            user=self.user,
            payment_type="enrollment",
            reference_id=fee.id,
            amount=fee.amount,
            status="completed"
        )
        self.assertEqual(str(transaction), f"enrollment - {transaction.amount} Gdes - completed")
        self.assertEqual(transaction.reference_id, fee.id)
        self.assertEqual(transaction.payment_type, "enrollment")