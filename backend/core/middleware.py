from django.conf import settings
from django.apps import apps
from .utils.current import (
    set_current_user, clear_current_user,
    set_current_academic_year, clear_current_academic_year,
)

class CurrentUserMiddleware:
    """
    Stocke l'utilisateur courant en thread-local pour le mixin d'audit.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, "user", None)
        if user and getattr(user, "is_authenticated", False):
            set_current_user(user)
        else:
            set_current_user(None)
        try:
            response = self.get_response(request)
        finally:
            clear_current_user()
        return response


class ActiveAcademicYearMiddleware:
    """
    Injecte l'année académique active dans request.academic_year
    et en thread-local (core.utils.current).

    Sélection de l'année:
      - Priorité: paramètre ?ay=<id> ou header 'X-Academic-Year-ID'
      - Sinon: première avec is_active=True (si le champ existe)
      - Sinon: fallback au plus récent (start_date desc, sinon id desc)

    Le modèle est configurable via settings.CORE_ACADEMIC_YEAR_MODEL,
    ex: "students.AcademicYear" ou "academics.AcademicYear".
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        model_path = getattr(settings, "CORE_ACADEMIC_YEAR_MODEL", "students.AcademicYear")
        ay = None

        try:
            AcademicYear = apps.get_model(model_path)
        except Exception:
            AcademicYear = None

        if AcademicYear:
            override_id = request.GET.get("ay") or request.headers.get("X-Academic-Year-ID")
            try:
                if override_id:
                    ay = AcademicYear.objects.filter(pk=override_id).first()
                if ay is None and any(f.name == "is_active" for f in AcademicYear._meta.fields):
                    ay = AcademicYear.objects.filter(is_active=True).first()
                if ay is None:
                    if any(f.name == "start_date" for f in AcademicYear._meta.fields):
                        ay = AcademicYear.objects.order_by("-start_date").first()
                    else:
                        ay = AcademicYear.objects.order_by("-id").first()
            except Exception:
                ay = None

        request.academic_year = ay
        set_current_academic_year(ay)
        try:
            response = self.get_response(request)
        finally:
            clear_current_academic_year()
        return response