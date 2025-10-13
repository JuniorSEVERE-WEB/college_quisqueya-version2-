# backend/core/permissions.py
from rest_framework import permissions


class IsAbonneOrStudentOrProf(permissions.BasePermission):
    """
    Autorise l'accès aux utilisateurs ayant un rôle :
    - abonne
    - student
    - professor
    - admin
    """

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role in ["abonne", "student", "professor", "admin"]
        )
