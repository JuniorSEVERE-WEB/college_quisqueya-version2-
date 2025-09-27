from django.urls import path
from . import views

app_name = "communication"

urlpatterns = [
    path("inbox/", views.inbox, name="inbox"),
    path("sent/", views.sent_messages, name="sent"),
    path("compose/", views.compose_message, name="compose"),
    path("<int:pk>/", views.message_detail, name="detail"),
    path("unread-count/", views.unread_count, name="unread_count"),
]
