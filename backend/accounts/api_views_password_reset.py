# backend/accounts/api_views_password_reset.py
from django.contrib.auth.forms import PasswordResetForm
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


@method_decorator(csrf_exempt, name="dispatch")
class PasswordResetAPIView(APIView):
    """
    Vue API pour la réinitialisation de mot de passe sans CSRF
    """

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        if not email:
            return Response({"error": "Email manquant."}, status=status.HTTP_400_BAD_REQUEST)

        form = PasswordResetForm({"email": email})
        if form.is_valid():
            form.save(
                request=request,
                email_template_name="registration/password_reset_email.html",
                subject_template_name="registration/password_reset_subject.txt",
            )
            return Response({"success": "Lien envoyé à l'adresse email."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Aucun utilisateur trouvé avec cet email."}, status=status.HTTP_400_BAD_REQUEST)
