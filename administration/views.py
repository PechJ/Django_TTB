from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from devices.models import Device
from django.http import HttpResponse
from django.views.decorators.http import require_POST


@login_required
def administration(request):
    context = {"route": "administration_home"}
    return render(request, "administration.html", context)


@login_required
def administration_funk(request):
    context = {"route": "administration_funk"}
    return render(request, "administration_funk.html", context)


@login_required
def administration_pager(request):
    context = {"route": "administration_pager"}
    return render(request, "administration_pager.html", context)


@login_required
def admin_funk_detail(request, pk):
    device = get_object_or_404(Device, pk=pk)
    return render(request, "admin_funk_detail.html", {'device': device})


@login_required
def administration_user(request):
    # Holt alle Benutzer aus der Datenbank
    all_users = User.objects.all()
    print(("Die Nutzer: ", User.objects.all()))
    
    # Übergibt die Benutzer im "Context" an das HTML-Template
    context = {
        'all_users': all_users
    }
    return render(request, 'administration_nutzer.html', context)


@login_required
def administration_funk(request):
    devices = Device.objects.exclude(
        eg_typ="TPG2200"
    ).order_by("geraetename")

    return render(
        request,
        "administration_funk.html",
        {
            "devices": devices,
            "route": "administration_funk",
        },
    )
    

@login_required
@require_POST
def update_device_field(request, pk):
    device = get_object_or_404(Device, pk=pk)
    
    # Prüfen, ob das Feld 'bos_sika_name' geschickt wurde
    if 'bos_sika_name' in request.POST:
        device.bos_sika_name = request.POST.get('bos_sika_name')
        device.save()
        
    # HTMX erwartet eine Antwort. Ein leerer HTTP 200 reicht aus.
    return HttpResponse(status=200)