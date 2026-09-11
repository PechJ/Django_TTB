from django.shortcuts import render, redirect, get_object_or_404
from .models import Device, ImportStatus, PagerReparatur
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
from .exports.pdf_exporter import PagerReparaturPdfGenerator


def device_list(request):
    devices = Device.objects.exclude(
        eg_typ="TPG2200"
    ).order_by("geraetename")
    
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


def pager_list(request):
    devices = Device.objects.filter(
        eg_typ="TPG2200"
    )

    tei = request.GET.get("tei", "").strip()
    seriennummer = request.GET.get("seriennummer", "").strip()
    geraetename = request.GET.get("geraetename", "").strip()
    software_version = request.GET.get("software_version", "").strip()
    issi = request.GET.get("issi", "").strip()
    landkreis = request.GET.get("landkreis", "").strip()
    dienststelle = request.GET.get("dienststelle", "").strip()
    heimat_dienststelle = request.GET.get("heimat_dienststelle", "").strip()
    eigentuemer = request.GET.get("eigentuemer", "").strip()
    nutzer = request.GET.get("nutzer", "").strip()
    bemerkung = request.GET.get("bemerkung", "").strip()
    status = request.GET.get("status", "").strip()

    if tei:
        devices = devices.filter(tei__icontains=tei)

    if seriennummer:
        devices = devices.filter(
            seriennummer__icontains=seriennummer
        )

    if geraetename:
        devices = devices.filter(
            geraetename__icontains=geraetename
        )

    if software_version:
        devices = devices.filter(
            software_version__icontains=software_version
        )

    if issi:
        devices = devices.filter(issi__icontains=issi)

    if landkreis:
        devices = devices.filter(
            landkreis__icontains=landkreis
        )

    if dienststelle:
        devices = devices.filter(
            dienststelle__icontains=dienststelle
        )

    if heimat_dienststelle:
        devices = devices.filter(
            heimat_dienststelle__icontains=heimat_dienststelle
        )

    if eigentuemer:
        devices = devices.filter(
            eigentuemer__icontains=eigentuemer
        )

    if nutzer:
        devices = devices.filter(
            nutzer__icontains=nutzer
        )

    if bemerkung:
        devices = devices.filter(
            bemerkung__icontains=bemerkung
        )

    if status:
        devices = devices.filter(status=status)

    devices = devices.order_by("geraetename")

    return render(
        request,
        "devices/pager_list.html",
        {
            "devices": devices,
            "tei": tei,
            "seriennummer": seriennummer,
            "geraetename": geraetename,
            "software_version": software_version,
            "issi": issi,
            "landkreis": landkreis,
            "dienststelle": dienststelle,
            "heimat_dienststelle": heimat_dienststelle,
            "eigentuemer": eigentuemer,
            "nutzer": nutzer,
            "bemerkung": bemerkung,
            "status": status,
        },
    )


def pager_detail(request, device_id):

    device = get_object_or_404(
        Device,
        id=device_id,
        eg_typ="TPG2200",
    )

    if request.method == "POST":

        device.seriennummer = request.POST.get(
            "seriennummer",
            "",
        ).strip()

        device.eigentuemer = request.POST.get(
            "eigentuemer",
            "",
        ).strip()

        device.nutzer = request.POST.get(
            "nutzer",
            "",
        ).strip()

        device.bemerkung = request.POST.get(
            "bemerkung",
            "",
        ).strip()

        device.save()

        messages.success(
            request,
            f"{device.geraetename} wurde gespeichert.",
        )

        return redirect(
            "devices:pager_detail",
            device_id=device.id,
        )

    return render(
        request,
        "devices/pager_detail.html",
        {
            "device": device,
        },
    )


def pager_reparatur_start(request, device_id):
    device = get_object_or_404(
        Device,
        id=device_id,
        eg_typ="TPG2200",
    )

    if request.method == "POST":
        
        print(">>> REPARATUR POST ANGEKOMMEN")
        
        # Seriennummer nur dann aus dem Formular übernehmen,
        # wenn in der Datenbank noch keine vorhanden ist.
        if not device.seriennummer:
            seriennummer = request.POST.get(
                "seriennummer",
                "",
            ).strip()

            if not seriennummer:
                messages.error(
                    request,
                    "Bitte eine Seriennummer eingeben.",
                )
                return render(
                    request,
                    "devices/pager_reparatur_start.html",
                    {"device": device},
                )

            device.seriennummer = seriennummer

        # Reparaturart aus Formular holen
        reparaturarten = request.POST.getlist("reparaturart")

        # Rechnungsadresse bestimmen
        if "Garantie" in reparaturarten:
            rechnungsadresse = Constants.MOTOROLA_RECHNUNGSADRESSE
        else:
            rechnungsadresse = request.POST.get(
                "rechnungsadresse",
                "",
            ).strip()

            if not rechnungsadresse:
                messages.error(
                    request,
                    "Bitte eine Rechnungsadresse eingeben.",
                )
                return render(
                    request,
                    "devices/pager_reparatur_start.html",
                    {"device": device},
                )

        # Gerät auf "In Reparatur" setzen
        device.status = Device.Status.IN_REPARATUR
        device.save()

        # Reparatur anlegen
        reparatur = PagerReparatur.objects.create(
            pager=device,
            artikel_modellnummer=device.eg_typ,
            option_features="siehe rechts (Leistungsmerkmale Pager)",
            rechnungsadresse=rechnungsadresse,
            symptome=request.POST.getlist("symptome"),
            reparaturart=reparaturarten,
            zubehoer=request.POST.getlist("zubehoer"),
            plombennummern=request.POST.get(
                "plombennummern",
                "",
            ).strip(),
            defektbeschreibung=request.POST.get(
                "defektbeschreibung",
                "",
            ).strip(),
            bemerkung=request.POST.get(
                "bemerkung",
                "",
            ).strip(),
        )

        # Reparatur-PDF erzeugen
        PagerReparaturPdfGenerator(
            reparatur
        ).generate()

        messages.success(
            request,
            f"Reparatur für {device.geraetename} wurde angelegt.",
        )

        return redirect(
            "devices:pager_detail",
            device_id=device.id,
        )

    return render(
        request,
        "devices/pager_reparatur_start.html",
        {"device": device},
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
            
            print("PAGER-FORMULAR IST GÜLTIG")

            uploaded_file = form.cleaned_data["file"]

            importer = PagerImporter(
                uploaded_file,
            )

            result = importer.run()
            
            print(
                f"PAGER-IMPORT: created={result.created}, "
                f"updated={result.updated}, "
                f"skipped={result.skipped}"
            )
            
            update_import_status(ImportType.PAGER)
            
            print("VOR MESSAGE")
            messages.success(
                request,
                f"{result.created} Pager angelegt, "
                f"{result.updated} aktualisiert."
            )
            print("NACH MESSAGE")

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

