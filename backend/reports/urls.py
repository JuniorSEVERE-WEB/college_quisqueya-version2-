from django.urls import path
from . import views
from .views import DashboardStatsAPIView
from .views import dashboard_view
from .views import dashboard_pdf_view

urlpatterns = [
    path(
        "report/<int:classroom_id>/<int:session_id>/",
        views.report_table,
        name="report_table",
    ),
    #path('web/<int:student_id>/', views.student_report_web, name='student_report_web'),
    path('pdf/<int:student_id>/', views.student_report_pdf, name='student_report_pdf'),
    path("api/dashboard-stats/", DashboardStatsAPIView.as_view(), name="dashboard-stats"),
    path("dashboard/", dashboard_view, name="dashboard"),
    path("dashboard/pdf/", views.dashboard_pdf_view, name="dashboard_pdf"),


]
