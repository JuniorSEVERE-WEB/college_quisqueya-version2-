from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from academics.models import Classroom
from .models import Message, ContactMessage
from .forms import MessageForm
from django.http import JsonResponse
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .serializers import ContactMessageSerializer



User = get_user_model()

@login_required
def inbox(request):
    msgs = request.user.received_messages.all().order_by("-created_at")
    return render(request, "communication/inbox.html", {"messages": msgs})

@login_required
def sent_messages(request):
    msgs = request.user.sent_messages.all().order_by("-created_at")
    return render(request, "communication/sent.html", {"messages": msgs})

@login_required
def message_detail(request, pk):
    msg = get_object_or_404(Message, pk=pk)
    if request.user in msg.recipients.all() and request.user not in msg.read_by.all():
        msg.read_by.add(request.user)
    return render(request, "communication/message_detail.html", {"message": msg})





def unread_count(request):
    if request.user.is_authenticated:
        count = request.user.received_messages.exclude(read_by=request.user).count()
        return {"unread_count": count}
    return {"unread_count": 0}


@login_required
def compose_message(request):
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = request.user
            msg.save()

            recipient_type = form.cleaned_data["recipient_type"]

            if recipient_type == "individual":
                msg.recipients.set(form.cleaned_data["recipients"])
            elif recipient_type == "class":
                classroom = form.cleaned_data["classroom"]
                if classroom:
                    msg.recipients.set(User.objects.filter(classroom=classroom))
            elif recipient_type == "all_students":
                msg.recipients.set(User.objects.filter(role="student"))
            elif recipient_type == "all_alumni":
                msg.recipients.set(User.objects.filter(role__in=["alumni_student", "alumni_prof", "alumni_employee"]))
            elif recipient_type == "all_staff":
                msg.recipients.set(User.objects.filter(role__in=["prof", "employee", "admin"]))

            msg.save()
            messages.success(request, "Message envoyé avec succès ✅")

            # 🔔 Notifier chaque destinataire
            channel_layer = get_channel_layer()
            for r in msg.recipients.all():
                unread_count = r.received_messages.exclude(read_by=r).count()
                async_to_sync(channel_layer.group_send)(
                    f"user_{r.id}",
                    {
                        "type": "send_notification",
                        "message": f"Nouveau message de {request.user.username}",
                        "count": unread_count,
                    }
                )

            return redirect("communication:sent")
    else:
        form = MessageForm()

    return render(request, "communication/compose.html", {"form": form})




