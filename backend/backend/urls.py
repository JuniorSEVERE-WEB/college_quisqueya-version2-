from django.contrib import admin
from django.urls import path, include
from django.views.i18n import set_language
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # ---- API publiques (sans authentification) ----
    path("api/", include("programs.api_urls")),    # classes publiques
    path("api/academics/", include("academics.api_urls")),  # si tu veux aussi exposer active classrooms

    # ---- API privées (auth requise) ----
    path("api/", include("students.urls")),
    path("api/", include("professors.urls")),
    path("api/", include("employees.urls")),
    path("api/", include("programs.urls")),        # ViewSets protégés
    path("api/", include("academics.urls")),
    path("api/payments/", include("payments.api_urls")),
    path("api/blog/", include("blog.api_urls")),
    path("api/reports/", include("reports.api_urls")),
    path("api/alumni/", include("alumni.api_urls")),
    path("api/communication/", include("communication.api_urls")),
    path('api/auth/', include('accounts.api_urls')),

    # ---- Apps non-API ----
    path("blog/", include("blog.urls")),
    path('payments/', include(('payments.urls', 'payments'), namespace='payments')),
    path("messages/", include(("communication.urls", "communication"), namespace="communication")),
    path("i18n/set-language/", set_language, name="set_language"),
    path("core/", include("core.urls")),
    path('reports/', include('reports.urls')),
    path('chaining/', include('smart_selects.urls')),

    # ---- JWT Auth ----
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # ---- Docs ----
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
