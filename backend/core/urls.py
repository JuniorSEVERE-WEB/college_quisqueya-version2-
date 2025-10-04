from django.urls import path
from .views import core_debug
from . import  views_dashboard

urlpatterns = [
    path("debug/", core_debug, name="core_debug"),
    path("dashboard/stats/", views_dashboard.dashboard_stats, name="dashboard-stats"),
]