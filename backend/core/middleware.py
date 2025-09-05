from academics.models import AcademicYear

def get_current_academic_year():
    try:
        return AcademicYear.objects.get(is_active=True)
    except AcademicYear.DoesNotExist:
        return None

class AcademicYearMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.academic_year = get_current_academic_year()
        return self.get_response(request)
