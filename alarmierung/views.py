from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from devices.models import SirenFRTStatus
from alarmierung.models import SirenFRTFreigabePending


@login_required
def home(request):
    return render(request, "alarmierung/home.html")


@login_required
def sirenen(request):
    status = SirenFRTStatus.objects.all().order_by("id")
    pending_freigaben = SirenFRTFreigabePending.objects.all().order_by("id")

    return render(
        request,
        "alarmierung/sirenen.html",
        {
            "status": status,
            "pending_freigaben": pending_freigaben,
        },
    )