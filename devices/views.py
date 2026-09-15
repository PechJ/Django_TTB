from django.shortcuts import render, redirect, get_object_or_404
from .models import Device, ImportStatus, PagerReparatur, Historie, Checkliste, Checklistenpunkt
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
from django.utils import timezone


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


def dashboard(request):
    devices = Device.objects.exclude(
        eg_typ="TPG2200"
    ).prefetch_related("checklisten__punkte")

    offene_checklisten = []

    for device in devices:
        checkliste = (
            device.checklisten
            .order_by("-import_am", "-id")
            .first()
        )

        if checkliste and not checkliste.vollstaendig:
            offene_checklisten.append({
                "device": device,
                "checkliste": checkliste,
            })

    return render(
        request,
        "devices/dashboard.html",
        {
            "offene_checklisten": offene_checklisten,
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


def pager_historie(request, device_id):
    device = get_object_or_404(
        Device,
        id=device_id,
        eg_typ="TPG2200",
    )

    historie = Historie.objects.filter(
        geraet=device,
    ).order_by(
        "-zeitpunkt",
    )

    return render(
        request,
        "devices/pager_historie.html",
        {
            "device": device,
            "historie": historie,
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

    reparatur = PagerReparatur.objects.filter(
        pager=device,
        status=PagerReparatur.Status.OFFEN,
    ).order_by("-begonnen_am").first()

    return render(
        request,
        "devices/pager_detail.html",
        {
            "device": device,
            "reparatur": reparatur,
        },
    )


def pager_reparatur_rueckkehr(request, reparatur_id):
    reparatur = get_object_or_404(
        PagerReparatur,
        id=reparatur_id,
        status=PagerReparatur.Status.OFFEN,
    )

    device = reparatur.pager

    if request.method == "POST":

        # Reparatur abschließen
        reparatur.status = PagerReparatur.Status.ABGESCHLOSSEN
        reparatur.zurueck_am = timezone.now()
        reparatur.save()

        # Historie schreiben
        Historie.objects.create(
            geraet=device,
            benutzer=request.user if request.user.is_authenticated else None,
            ereignis="Reparatur abgeschlossen",
            details="Pager aus Reparatur zurück und wieder in Betrieb.",
        )

        # Pager wieder in Betrieb nehmen
        device.status = Device.Status.IN_BETRIEB
        device.save()

        messages.success(
            request,
            f"{device.geraetename} ist wieder in Betrieb.",
        )

        return redirect(
            "devices:pager_detail",
            device_id=device.id,
        )

    return render(
        request,
        "devices/pager_reparatur_rueckkehr.html",
        {
            "reparatur": reparatur,
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

        Historie.objects.create(
            geraet=device,
            benutzer=request.user if request.user.is_authenticated else None,
            ereignis="Reparatur gestartet",
            details=(
                f"Reparaturart: {', '.join(reparaturarten)}\n"
                f"Symptome: {', '.join(reparatur.symptome)}\n"
                f"Defektbeschreibung: {reparatur.defektbeschreibung}\n"
                f"Interne Bemerkung: {reparatur.bemerkung}"
            ),
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


def device_detail(request, device_id):
    device = get_object_or_404(
        Device.objects.exclude(eg_typ="TPG2200"),
        id=device_id,
    )

    checkliste = (
        device.checklisten
        .prefetch_related("punkte")
        .order_by("-import_am", "-id")
        .first()
    )

    return render(
        request,
        "devices/device_detail.html",
        {
            "device": device,
            "checkliste": checkliste,
        },
    )
    
    
def checklist_punkt_toggle(request, device_id, punkt_id):
    if request.method != "POST":
        return redirect("devices:device_detail", device_id=device_id)

    device = get_object_or_404(
        Device.objects.exclude(eg_typ="TPG2200"),
        id=device_id,
    )

    checkliste = get_object_or_404(
        Checkliste,
        geraet=device,
        id=request.POST.get("checkliste_id"),
    )

    punkt = get_object_or_404(
        Checklistenpunkt,
        id=punkt_id,
        checkliste=checkliste,
    )

    # Persönliche Abholung
    if punkt.code == "PERSOENLICHE_ABHOLUNG" and not punkt.erledigt:
        punkt.erledigt = True
        punkt.erledigt_am = timezone.now()
        punkt.erledigt_von = (
            request.user if request.user.is_authenticated else None
        )
        punkt.save()

        # Die beiden Postversand-Punkte werden nicht mehr benötigt.
        checkliste.punkte.filter(
            code__in=[
                "POSTVERSAND_GESPERRT",
                "POSTVERSAND_ENTSPERRT",
            ]
        ).update(erforderlich=False)

        return redirect(
            "devices:device_detail",
            device_id=device_id,
        )

    # Funkgerät programmiert
    if punkt.code == "FUNKGERAET_PROGRAMMIERT" and not punkt.erledigt:
        punkt.erledigt = True
        punkt.erledigt_am = timezone.now()
        punkt.erledigt_von = (
            request.user if request.user.is_authenticated else None
        )
        punkt.save()

        # Aktuelle Programmversion im Gerät hinterlegen
        device.software_version = Constants.REQUIRED_FIRMWARE
        device.programming_date = timezone.now()
        device.assigned_to = (
            request.user if request.user.is_authenticated else None
        )

        device.save(
            update_fields=[
                "software_version",
                "programming_date",
                "assigned_to",
            ]
        )

        # Historie
        Historie.objects.create(
            geraet=device,
            benutzer=(
                request.user
                if request.user.is_authenticated
                else None
            ),
            ereignis="Funkgerät programmiert",
            details=(
                f"Programmversion: "
                f"{Constants.REQUIRED_FIRMWARE}"
            ),
        )

        return redirect(
            "devices:device_detail",
            device_id=device_id,
        )

    # Normaler Checklistenpunkt
    punkt.erledigt = not punkt.erledigt

    if punkt.erledigt:
        punkt.erledigt_am = timezone.now()
        punkt.erledigt_von = (
            request.user if request.user.is_authenticated else None
        )
    else:
        punkt.erledigt_am = None
        punkt.erledigt_von = None

    punkt.save()

    return redirect(
        "devices:device_detail",
        device_id=device_id,
    )