from django import forms
from .models import EnrollmentFee, Donation

class EnrollmentFeeForm(forms.ModelForm):
    class Meta:
        model = EnrollmentFee
        fields = ["academic_year", "amount"]


class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ["name", "email", "amount", "message"]
