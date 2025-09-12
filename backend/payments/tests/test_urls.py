from django.test import SimpleTestCase
from django.urls import reverse, resolve
from payments import views

class PaymentsUrlsTests(SimpleTestCase):
    def test_pay_enrollment_fee_url_resolves(self):
        url = reverse("payments:pay_enrollment_fee")
        self.assertEqual(resolve(url).func, views.pay_enrollment_fee)

    def test_make_donation_url_resolves(self):
        url = reverse("payments:make_donation")
        self.assertEqual(resolve(url).func, views.make_donation)

    def test_payment_success_url_resolves(self):
        url = reverse("payments:payment_success")
        self.assertEqual(resolve(url).func, views.payment_success)