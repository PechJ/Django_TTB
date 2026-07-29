from django.shortcuts import render
from .models import Device
from django.contrib import messages
from devices.forms import ImportForm
from devices.validators.input_validator import InputValidator
from devices.imports.manufacturer_radio import ManufacturerImporter
from devices.forms import ManufacturerRadioImportForm
from devices.imports.excel_reader import ExcelReader
from devices.imports.device_importer import DeviceImporter
from devices.constants import DeviceConstants as Constants
from devices.imports.excel_reader import ImportType


def device_list(request):
    devices = Device.objects.all().order_by("geraetename")

    return render(
        request,
        "devices/device_list.html",
        {"devices": devices},
    )


def manufacturer_import_view(request):

    form = ManufacturerRadioImportForm()

    if request.method == "POST":

        form = ManufacturerRadioImportForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():

            uploaded_file = form.cleaned_data["file"]

            importer = ManufacturerImporter(
                uploaded_file,
            )

            result = importer.run()

            messages.success(
                request,
                f"{result.created} Geräte angelegt, "
                f"{result.updated} aktualisiert."
            )

    return render(
        request,
        "devices/import_radio.html",
        {
            "form": form,
        },
    )

    
def import_view(request):

    form = ImportForm()

    if request.method == "POST":

        form = ImportForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():

            uploaded_file = form.cleaned_data["file"]

            rows, import_type = ExcelReader(uploaded_file).read()

            validator = InputValidator(rows)

            errors = validator.validate()

            if errors:

                for error in errors:

                    messages.error(
                        request,
                        f"Zeile {error['row']}: {error['message']}"
                    )

            else:

                if import_type == import_type.ENDGERAETE:
                    importer = DeviceImporter(rows)
                    exporter = EndgeraeteExporter()

                elif import_type == import_type.SIRENEN:
                    importer = SirenImporter(rows)
                    exporter = SirenenExporter()

                else:
                    messages.error(
                        request,
                        "Unbekannter Antragstyp."
                    )
                    return render(
                        request,
                        "devices/import.html",
                        {"form": form},
                    )

                result = importer.run()
                exporter.run()

                messages.success(
                    request,
                    f"{result.created} Geräte angelegt, {result.updated} aktualisiert."
                )
                
                for row in rows:
                    print(row)

    return render(
        request,
        "devices/import.html",
        {
            "form": form,
        },
    )
    

def funk_home(request):

    return render(
        request,
        "devices/funk_home.html",
    )
    

def programming_list(request):

    devices = Device.objects.exclude(
        software_version=Constants.REQUIRED_FIRMWARE
    ).order_by(
        "organisationsname",
        "funkrufname",
    )
    
    return render(
        request,
        "devices/programming_list.html",
        {
            "devices": devices,
        },
    )
    

def programming_complete(request, device_id):    
    from django.shortcuts import get_object_or_404, redirect
    from django.utils import timezone
    
    if request.method != "POST":
        return redirect("devices:programming_list")
    
    device = get_object_or_404(Device, id=device_id)

    device.software_version = Constants.REQUIRED_FIRMWARE
    device.programming_date = timezone.now()
    device.assigned_to = request.user

    device.save()
    messages.success(
    request,
    f"{device.geraetename} wurde erfolgreich programmiert."
)

    return redirect("devices:programming_list")

