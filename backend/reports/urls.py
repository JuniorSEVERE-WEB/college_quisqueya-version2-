from django.urls import path
from . import views

urlpatterns = [
    path(
        "report/<int:classroom_id>/<int:session_id>/",
        views.report_table,
        name="report_table",
    ),
    #path('web/<int:student_id>/', views.student_report_web, name='student_report_web'),
    path('pdf/<int:student_id>/', views.student_report_pdf, name='student_report_pdf'),


]
