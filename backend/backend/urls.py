"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.i18n import set_language
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include("students.urls")), 
    path("api/", include("professors.urls")),
    path("api/", include("employees.urls")),
    path("api/", include("programs.urls")),
    path("blog/", include("blog.urls")),
    path('payments/', include(('payments.urls', 'payments'), namespace='payments')),
    path("messages/", include(("communication.urls", "communication"), namespace="communication")),
    path('api/academics/', include('academics.urls')),
    path('chaining/', include('smart_selects.urls')),
    path("i18n/set-language/", set_language, name="set_language"),
    path("core/", include("core.urls")),
    path('reports/', include('reports.urls')),
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
