# backend/backend/urls.py

from django.contrib import admin
from django.urls import path, include
from django.views.i18n import set_language
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from django.contrib.auth import views as auth_views
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect, HttpResponse


# ================================
# 👇 PAGE D’ACCUEIL DU BACKEND
# ================================
def home(request):
    """Page d’accueil simple pour Render ou tests backend"""
    html = """
    <html>
        <head><title>Collège Quisqueya - Backend</title></head>
        <body style="font-family:Arial; text-align:center; padding-top:50px;">
            <h1>Bienvenue sur le backend Collège Quisqueya 🎓</h1>
            <p>API opérationnelle avec Django REST Framework.</p>
            <p><a href="/admin/">👉 Accéder à l’administration</a></p>
            <p><a href="/api/docs/">📘 Documentation API (Swagger)</a></p>
        </body>
    </html>
    """
    return HttpResponse(html)


urlpatterns = [
    # ---- Page d’accueil ----
    path("", home, name="home"),  # ✅ Corrige le 404 sur Render

    # ---- Admin ----
    path("admin/", admin.site.urls),

    # ---- API publiques ----
    path("api/schoollife/", include("schoollife.api_urls")),   # Vie scolaire
    path("api/homepage/", include("homepage.api_urls")),
    path("api/programs/", include("programs.api_urls")),       # Programmes publics
    path("api/academics/", include("academics.api_urls")),     # Année académique et classes actives
    path("api/classrooms/", include("programs.api_urls")),
    path("api/subjects/", include("programs.api_urls")),
    path("api/", include("programs.api_urls")),
    path("api/", include("communication.api_urls")),
    path("api/professors/", include("professors.api_urls")),
    path("api/employees/", include("employees.api_urls")),
    path("api/students/", include("students.api_urls")),
    path("api/", include("blog.api_urls")),
    path("api/students/", include("students.urls")),

    # ---- API privées (auth requise) ----
    path("api/", include("students.urls")),
    path("api/", include("professors.urls")),
    path("api/", include("employees.urls")),
    path("api/", include("programs.urls")),
    path("api/", include("academics.urls")),
    path("api/payments/", include("payments.api_urls")),
    path("api/blog/", include("blog.api_urls")),
    path("api/reports/", include("reports.api_urls")),
    path("api/alumni/", include("alumni.api_urls")),
    path("api/", include("communication.api_urls")),
    path("api/communication/", include("communication.api_urls")),

    # ---- Auth & comptes ----
    path("api/auth/", include("accounts.api_urls")),

    # ---- Apps non-API ----
    path("blog/", include("blog.urls")),
    path("payments/", include(("payments.urls", "payments"), namespace="payments")),
    path("messages/", include(("communication.urls", "communication"), namespace="communication")),
    path("i18n/set-language/", set_language, name="set_language"),
    path("reports/", include("reports.urls")),
    path("chaining/", include("smart_selects.urls")),
    path("api/", include("about.urls")),
    path("api/core/", include("core.urls")),

    # ---- JWT Auth ----
    path("api/auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/auth/token/verify/", TokenVerifyView.as_view(), name="token_verify"),

    # ---- Documentation API ----
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),

    # ---- Mot de passe oublié ----
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="registration/password_reset_form.html",
            email_template_name="registration/password_reset_email.html",
            subject_template_name="registration/password_reset_subject.txt",
            success_url="/password-reset/done/",
        ),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="registration/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="registration/password_reset_confirm.html",
            success_url="/reset/done/",
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="registration/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]


# ---- Fichiers médias en mode DEBUG ----
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
