from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
        widgets = {
            'birth_certificate': forms.ClearableFileInput(attrs={
                'accept': 'application/pdf',
                'max-file-size': '3145728',  # 3 MB in bytes
            }),
            'last_school_report': forms.ClearableFileInput(attrs={
                'accept': 'application/pdf',
                'max-file-size': '3145728',
            }),
        }
        help_texts = {
            'birth_certificate': "Format PDF uniquement, taille maximale 3 MB.",
            'last_school_report': "Format PDF uniquement, taille maximale 3 MB."
        }

    def clean_birth_certificate(self):
        file = self.cleaned_data.get('birth_certificate')
        if file:
            if file.size > 3 * 1024 * 1024:
                raise forms.ValidationError("Le fichier ne doit pas dépasser 3 MB.")
            if not file.name.lower().endswith('.pdf'):
                raise forms.ValidationError("Le fichier doit être au format PDF.")
        return file

    def clean_last_school_report(self):
        file = self.cleaned_data.get('last_school_report')
        if file:
            if file.size > 3 * 1024 * 1024:
                raise forms.ValidationError("Le fichier ne doit pas dépasser 3 MB.")
            if not file.name.lower().endswith('.pdf'):
                raise forms.ValidationError("Le fichier doit être au format PDF.")
        return file
