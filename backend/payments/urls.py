from django.urls import path
from . import views

app_name = "payments"

urlpatterns = [
    path("enrollment/", views.pay_enrollment_fee, name="pay_enrollment_fee"),
    path("donation/", views.make_donation, name="make_donation"),
    path("success/", views.payment_success, name="payment_success"),
]
