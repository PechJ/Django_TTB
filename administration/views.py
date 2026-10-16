from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from devices.models import Device
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from .imports.excel_reader import ExcelReader
from devices.imports.device_importer import AdminDeviceImporter
from django.contrib import messages
from django import forms


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
    
    all_users = User.objects.all()
    print(("Die Nutzer: ", User.objects.all()))
    
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
    
    try:
        device = Device.objects.get(pk=pk)
    except Device.DoesNotExist:
        return HttpResponse("Gerät wurde in der DB nicht gefunden!", status=404)
    
    if 'eg_art' in request.POST:
        device.eg_art = request.POST.get('eg_art')
        device.save()
        
    if 'seriennummer' in request.POST:
        device.seriennummer = request.POST.get('seriennummer')
        device.save()
        
    if 'issi' in request.POST:
            device.issi = request.POST.get('issi')
            device.save()
            
    if 'bos_sika_nummer' in request.POST:
            device.bos_sika_nummer = request.POST.get('bos_sika_nummer')
            device.save()
            
    if 'bos_sika_name' in request.POST:
            device.bos_sika_name = request.POST.get('bos_sika_name')
            device.save()
            
    if 'landkreis' in request.POST:
            device.landkreis = request.POST.get('landkreis')
            device.save()
            
    if 'kommune' in request.POST:
            device.kommune = request.POST.get('kommune')
            device.save()
        
    if 'organisationsart' in request.POST:
                device.organisationsart = request.POST.get('organisationsart')
                device.save()
                
    if 'organisationsname' in request.POST:
                device.organisationsname = request.POST.get('organisationsname')
                device.save()
                
    if 'fahrzeugart' in request.POST:
                device.fahrzeugart = request.POST.get('fahrzeugart')
                device.save()
                
    if 'funkrufname' in request.POST:
                    device.funkrufname = request.POST.get('funkrufname')
                    device.save()
                    
    if 'verwendung' in request.POST:
                    device.verwendung = request.POST.get('verwendung')
                    device.save()
                    
    if 'software_version' in request.POST:
                    device.software_version = request.POST.get('software_version')
                    device.save()
                
    return HttpResponse(status=200)


@login_required
def administration_import(request):
    
    if request.method == "POST":

        form = ExcelReader(request.POST, request.FILES)

        if form.is_valid():
            try:

                data_rows = form.read()

                importer = AdminDeviceImporter(data_rows)
                result = importer.run()

                messages.success(
                    request,
                    f"{result.updated} Geräte aktualisiert, "
                    f"{result.skipped} nicht zugeordnet."
                )
            except Exception as e:
                messages.error(request, f"Fehler beim Importieren: {e}")
    else:
        
        form = ExcelReader()

    return render(
        request,
        "administration_import.html",
        {
            "form": form,
        },
        )