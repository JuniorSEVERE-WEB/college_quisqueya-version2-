from django.urls import path
from . import views

urlpatterns = [
    path(
        "report/<int:classroom_id>/<int:session_id>/",
        views.report_table,
        name="report_table",
    ),
]
