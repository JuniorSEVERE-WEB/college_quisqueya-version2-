from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Admin peut tout faire, les autres peuvent seulement lire.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff

class IsProfessorOrAdmin(permissions.BasePermission):
    """
    Professeur ou admin peut modifier, les autres seulement lire.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff or hasattr(request.user, 'professor')

class IsStudentOrAdmin(permissions.BasePermission):
    """
    Élève ou admin peut accéder, les autres non.
    """
    def has_permission(self, request, view):
        return request.user.is_staff or hasattr(request.user, 'student')