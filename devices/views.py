from django.shortcuts import render
from .models import Device
from django.contrib import messages
from devices.forms import ImportForm
from devices.validators.input_validator import InputValidator
from devices.imports.manufacturer_radio import ManufacturerImporter
from devices.forms import ManufacturerRadioImportForm
from devices.imports.excel_reader import ExcelReader
from devices.imports.device_importer import DeviceImporter


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

            rows = ExcelReader(
                uploaded_file,
            ).read()
            print(rows)

            validator = InputValidator(rows)

            errors = validator.validate()

            if errors:

                for error in errors:

                    messages.error(
                        request,
                        f"Zeile {error['row']}: {error['message']}"
                    )

            else:

                importer = DeviceImporter(rows)

                result = importer.run()

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