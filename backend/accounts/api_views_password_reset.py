from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

User = get_user_model()


@method_decorator(csrf_exempt, name="dispatch")
class PasswordResetAPIView(APIView):
    """
    Envoie un email avec un lien de réinitialisation pointant vers le frontend.
    POST /api/auth/password-reset/  { "email": "..." }
    """

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        if not email:
            return Response({"error": "Email manquant."}, status=status.HTTP_400_BAD_REQUEST)

        form = PasswordResetForm({"email": email})
        if form.is_valid():
            frontend_url = getattr(settings, "FRONTEND_URL", "http://localhost:5173")
            form.save(
                request=request,
                email_template_name="registration/password_reset_frontend_email.txt",
                subject_template_name="registration/password_reset_subject.txt",
                extra_email_context={"frontend_url": frontend_url},
                use_https=request.is_secure(),
            )
            return Response(
                {"success": "Lien de réinitialisation envoyé à l'adresse email."},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"error": "Aucun utilisateur trouvé avec cet email."},
            status=status.HTTP_400_BAD_REQUEST,
        )


@method_decorator(csrf_exempt, name="dispatch")
class PasswordResetConfirmAPIView(APIView):
    """
    Valide le token et change le mot de passe.
    POST /api/auth/password-reset-confirm/  { "uid": "...", "token": "...", "new_password1": "...", "new_password2": "..." }
    """

    def post(self, request, *args, **kwargs):
        uid = request.data.get("uid")
        token = request.data.get("token")
        password1 = request.data.get("new_password1")
        password2 = request.data.get("new_password2")

        if not all([uid, token, password1, password2]):
            return Response(
                {"error": "Données manquantes (uid, token, new_password1, new_password2)."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user_pk = urlsafe_base64_decode(uid).decode()
            user = User.objects.get(pk=user_pk)
        except (User.DoesNotExist, ValueError, OverflowError):
            return Response({"error": "Lien invalide."}, status=status.HTTP_400_BAD_REQUEST)

        if not default_token_generator.check_token(user, token):
            return Response({"error": "Le lien est invalide ou a expiré."}, status=status.HTTP_400_BAD_REQUEST)

        form = SetPasswordForm(user, {"new_password1": password1, "new_password2": password2})
        if form.is_valid():
            form.save()
            return Response({"success": "Mot de passe réinitialisé avec succès."}, status=status.HTTP_200_OK)

        return Response({"error": form.errors}, status=status.HTTP_400_BAD_REQUEST)
