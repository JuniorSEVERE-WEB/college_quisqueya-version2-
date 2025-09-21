from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import EnrollmentFee, Donation, Transaction
from .forms import EnrollmentFeeForm, DonationForm
from django.http import HttpResponse


import stripe
from django.conf import settings
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from django.http import HttpResponse

stripe.api_key = settings.STRIPE_SECRET_KEY

# Frais d’inscription
@login_required
def pay_enrollment_fee(request):
    if request.method == "POST":
        form = EnrollmentFeeForm(request.POST)
        if form.is_valid():
            fee = form.save(commit=False)
            fee.student = request.user
            fee.save()

            # Ajouter au transaction log
            Transaction.objects.create(
                user=request.user,
                payment_type="enrollment",
                reference_id=fee.id,
                amount=fee.amount
            )

            return redirect("payments:payment_success")
    else:
        form = EnrollmentFeeForm()
    return render(request, "payments/pay_enrollment_fee.html", {"form": form})


# Dons
def make_donation(request):
    if request.method == "POST":
        form = DonationForm(request.POST)
        if form.is_valid():
            donation = form.save(commit=False)
            if request.user.is_authenticated:
                donation.donor = request.user
            donation.save()

            # Ajouter au transaction log
            Transaction.objects.create(
                user=request.user if request.user.is_authenticated else None,
                payment_type="donation",
                reference_id=donation.id,
                amount=donation.amount
            )

            return redirect("payments:payment_success")
    else:
        form = DonationForm()
    return render(request, "payments/make_donation.html", {"form": form})


# Page succès
def payment_success(request):
    return HttpResponse("✅ Paiement réussi ! Merci.")
# Page echec

def payment_cancel(request):
    return HttpResponse("❌ Paiement annulé. Réessayez.")


@csrf_exempt
def create_checkout_session(request):
    try:
        # Exemple : frais d'inscription à 50 USD
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': 5000,  # en cents (50.00 USD)
                        'product_data': {
                            'name': 'Frais d’inscription',
                        },
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url='http://localhost:8000/payments/success/',
            cancel_url='http://localhost:8000/payments/cancel/',
        )
        return redirect(checkout_session.url)
    except Exception as e:
        return JsonResponse({'error': str(e)})
    

# ...existing code...
from rest_framework import viewsets, permissions
from .models import Donation, EnrollmentFee
from .serializers import DonationSerializer, EnrollmentFeeSerializer

class DonationViewSet(viewsets.ModelViewSet):
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer
    permission_classes = [permissions.IsAuthenticated]

class EnrollmentFeeViewSet(viewsets.ModelViewSet):
    queryset = EnrollmentFee.objects.all()
    serializer_class = EnrollmentFeeSerializer
    permission_classes = [permissions.IsAuthenticated]
# ...existing code...
