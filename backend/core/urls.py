# backend/core/urls.py
from django.urls import path
from .views import core_debug
from . import views_dashboard

urlpatterns = [
    path("debug/", core_debug, name="core_debug"),
    path("dashboard/stats/", views_dashboard.dashboard_stats, name="dashboard-stats"),
    path("dashboard/chart-data/", views_dashboard.dashboard_chart_data, name="dashboard-chart-data"),
    path("dashboard/recent/", views_dashboard.dashboard_recent, name="dashboard-recent"),
]
