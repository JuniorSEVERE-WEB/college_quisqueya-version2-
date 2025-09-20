from django.http import JsonResponse
from django.utils import timezone
from .utils.current import get_current_user, get_current_academic_year

def core_debug(request):
    user = get_current_user()
    ay = get_current_academic_year()
    return JsonResponse({
        "now": timezone.now().isoformat(),
        "language": getattr(request, "LANGUAGE_CODE", None),
        "request_user": request.user.username if request.user.is_authenticated else None,
        "threadlocal_user": user.username if user else None,
        "academic_year": {
            "id": getattr(ay, "id", None),
            "str": str(ay) if ay else None,
        },
        "hint": "Test ?ay=<id> ou header X-Academic-Year-ID",
    })