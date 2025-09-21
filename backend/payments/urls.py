from django.urls import include, path
from . import views

app_name = "payments"

urlpatterns = [
    path("enrollment/", views.pay_enrollment_fee, name="pay_enrollment_fee"),
    path("donation/", views.make_donation, name="make_donation"),
    path("success/", views.payment_success, name="payment_success"),
    path("cancel/", views.payment_cancel, name="payment_cancel"),
    path("create-checkout-session/", views.create_checkout_session, name="create_checkout_session")

]

