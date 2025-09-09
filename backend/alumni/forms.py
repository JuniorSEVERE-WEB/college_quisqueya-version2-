from django import forms
from .models import Alumni

class AlumniForm(forms.ModelForm):
    class Meta:
        model = Alumni
        fields = ("user", "role", "year_left", "promo_name", "years_interval", "proof_document")
        widgets = {
            "year_left": forms.NumberInput(attrs={"min": 1995, "max": 2100}),
            "years_interval": forms.TextInput(attrs={"placeholder": "2018-2025"}),
        }