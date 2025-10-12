from rest_framework.permissions import BasePermission


class IsAbonneOrStudentOrProf(BasePermission):
    """
    Autorise les utilisateurs avec les rôles 'abonne', 'student', 'prof'
    ✅ mais aussi les administrateurs (is_staff ou is_superuser)
    """

    message = (
        "⛔ Accès restreint : seuls les abonnés, étudiants, professeurs ou administrateurs peuvent consulter ces données."
    )

    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False

        # ✅ Les administrateurs peuvent tout voir
        if user.is_staff or user.is_superuser:
            return True

        allowed_roles = {"abonne", "student", "prof"}
        return user.role in allowed_roles
