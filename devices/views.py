from django.shortcuts import render
from .models import Device, ImportStatus
from django.contrib import messages
from devices.forms import ImportForm
from devices.validators.input_validator import InputValidator
from devices.imports.manufacturer_radio import ManufacturerImporter
from devices.forms import ManufacturerRadioImportForm, PagerImportForm
from devices.imports.excel_reader import ExcelReader
from devices.imports.device_importer import DeviceImporter
from devices.constants import DeviceConstants as Constants
from devices.imports.excel_reader import ImportType
from .utils import create_export_filename
from devices.exports.tactilon_radio_builder import TactilonRadioBuilder
from devices.exports.csv_exporter import CsvExporter
from devices.services.import_status import update_import_status
from devices.exports.radio_directory_exporter import RadioDirectoryExporter
from devices.imports.pager_importer import PagerImporter


def device_list(request):
    devices = Device.objects.all().order_by("geraetename")
    import_status = ImportStatus.objects.get(import_type="endgeraete")
    
    last_device_import = Device.objects.exclude(
        datum_ttb__isnull=True
    ).order_by("-datum_ttb").first()

    return render(
        request,
        "devices/device_list.html",
        {
            "devices": devices,
            "mcc": Constants.MCC,
            "mnc": Constants.MNC,
            "import_date": import_status.last_import,
            "last_device_import": last_device_import.datum_ttb if last_device_import else None,
        },
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


def pager_import_view(request):

    form = PagerImportForm()

    if request.method == "POST":

        form = PagerImportForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():

            uploaded_file = form.cleaned_data["file"]

            importer = PagerImporter(
                uploaded_file,
            )

            result = importer.run()
            
            update_import_status(ImportType.PAGER)

            messages.success(
                request,
                f"{result.created} Pager angelegt, "
                f"{result.updated} aktualisiert."
            )

    return render(
        request,
        "devices/import_pager.html",
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

                if import_type == ImportType.ENDGERAETE:

                    importer = DeviceImporter(rows)

                    result = importer.run()
                    
                    update_import_status(
                        ImportType.ENDGERAETE
                    )
                    
                    landkreis = rows[0]["landkreis"]

                    radio_exporter = RadioDirectoryExporter(
                        landkreis
                    )
                    
                    radio_exporter.export()

                    builder = TactilonRadioBuilder(rows)

                    headers, export_rows = builder.build()

                    filename = create_export_filename(
                        rows[0]["organisationsname"]
                    )

                    print(">>> CsvExporter wird aufgerufen")
                    filepath = CsvExporter(
                        headers=headers,
                        rows=export_rows,
                    ).export(filename)
                    print(filepath)

                elif import_type == ImportType.SIRENEN:
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

                messages.success(
                    request,
                    f"{result.created} Geräte angelegt, {result.updated} aktualisiert."
                )

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
    
    
def alarmierung_home(request):

    return render(
        request,
        "devices/alarmierung_home.html",
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

