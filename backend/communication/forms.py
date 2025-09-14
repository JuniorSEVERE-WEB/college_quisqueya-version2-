from django import forms
from django.contrib.auth import get_user_model
from academics.models import Classroom
from .models import Message

User = get_user_model()

class MessageForm(forms.ModelForm):
    recipient_type = forms.ChoiceField(
        choices=[
            ("individual", "Utilisateur(s) spécifique(s)"),
            ("class", "Classe"),
            ("all_students", "Tous les étudiants"),
            ("all_alumni", "Tous les alumni"),
            ("all_staff", "Tous les membres (profs, employés, admin)"),
        ],
        required=True
    )
    recipients = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )
    classroom = forms.ModelChoiceField(
        queryset=Classroom.objects.all(),
        required=False
    )

    class Meta:
        model = Message
        fields = ["subject", "body", "recipient_type", "recipients", "classroom"]