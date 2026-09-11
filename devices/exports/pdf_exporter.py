from pathlib import Path

from pypdf import PdfReader, PdfWriter

from devices.constants import DeviceConstants as Constants


class PagerReparaturPdfGenerator:
    """
    Erstellt das Motorola-Reparaturformular für einen Pager.
    """

    TEMPLATE_NAME = "02. Reparaturauftragsformular- Pager-.pdf"

    # -------------------------------------------------
    # Symptome -> PDF-Checkboxen
    # -------------------------------------------------

    SYMPTOM_FIELDS = {
        "Keine Funktion": "C13",
        "Display – Fehler": "C9",
        "Programmierung": "C17",
        "Batterie / Ladeprobleme": "C20",
        "Bucht nicht ein": "C14",
        "Schaden durch physischen Einfluss": "C10",
        "Kein / schlechter Empfang": "C18",
        "Dauerton": "C21",
        "Schaden durch Flüssigkeiten": "C15",
        "Keine / geringe Sendeleistung": "C11",
        "Keine Signalisierung": "C19",
        "Schaden durch Chemikalien": "C22",
        "Kein Ton/geringe Lautstärke": "C16",
        "Keine Rauschsperre": "C12",
    }

    # -------------------------------------------------
    # Reparaturart -> PDF-Radio
    # -------------------------------------------------

    REPAIR_TYPE_STATES = {
        "Vorabaustausch": "/0",
        "Kostenpflichtige Reparatur - mit Kostenvoranschlag": "/1",
        "Garantie": "/2",
        "Erneute Reparatur (90 Tage)": "/3",
        "Kostenpflichtige Reparatur - kein Kostenvoranschlag": "/4",
        "Sichere entsorgung des eingesendeten Digitalfunkgerätes wird gewünscht": "/5",
    }

    # -------------------------------------------------
    # Standard Leistungsmerkmale
    # -------------------------------------------------

    STANDARD_LEISTUNGSMERKMALE = (
        "---------------------------------------------------------------------------------------------\n"
        "Standard Leistungsmerkmale:\n"
        "GPS FEATURE, MSDS, OTA PAGER CONFIGURATION,\n"
        "PERMANENT DISABLE FEATURE, SCCH FEATURE, SDS\n"
        "REMOTE CONTROL, IMMEDIATE TEXT MESSAGE"
        )

    def __init__(self, reparatur):
        self.reparatur = reparatur
        self.device = reparatur.pager

    def generate(self):
        # -------------------------------------------------
        # PDF-Vorlage
        # -------------------------------------------------

        template_path = (
            Path(__file__).resolve().parent.parent
            / "pdf_templates"
            / self.TEMPLATE_NAME
        )

        if not template_path.exists():
            raise FileNotFoundError(
                f"PDF-Vorlage nicht gefunden: {template_path}"
            )

        # -------------------------------------------------
        # Seriennummer
        # -------------------------------------------------

        seriennummer = (
            self.device.seriennummer or ""
        ).strip()

        if not seriennummer:
            raise ValueError(
                "Der Pager besitzt keine Seriennummer."
            )

        # -------------------------------------------------
        # Downloads-Ordner
        # -------------------------------------------------

        downloads = Path.home() / "Downloads"
        downloads.mkdir(
            parents=True,
            exist_ok=True,
        )

        filename = (
            "02. Reparaturauftragsformular- Pager-"
            f"{seriennummer}.pdf"
        )

        output_path = downloads / filename

        # -------------------------------------------------
        # PDF laden
        # -------------------------------------------------

        reader = PdfReader(str(template_path))
        writer = PdfWriter()

        writer.clone_document_from_reader(reader)

        # -------------------------------------------------
        # Defektbeschreibung
        # -------------------------------------------------

        defektbeschreibung = (
            self.reparatur.defektbeschreibung or ""
        ).strip()

        if defektbeschreibung:
            defektbeschreibung = (
                defektbeschreibung
                + "\n\n"
                + self.STANDARD_LEISTUNGSMERKMALE
            )
        else:
            defektbeschreibung = (
                self.STANDARD_LEISTUNGSMERKMALE
            )

        # -------------------------------------------------
        # Normale Textfelder
        # -------------------------------------------------

        fields = {
            "Text Field IMP 3": Constants.MOTOROLA_KUNDENNUMMER,
            "Text Field IMP 5": Constants.MOTOROLA_FIRMA,
            "Text Field IMP 8": Constants.MOTOROLA_ORGANISATION,
            "Text Field IMP 7": self.reparatur.rechnungsadresse,
            "Text Field IMP 15": Constants.MOTOROLA_ANSPRECHPARTNER,
            "Text Field IMP 16": Constants.MOTOROLA_EMAILADRESSE,
            "Text Field IMP 17": Constants.MOTOROLA_TEL,
            "Text Field IMP 18": Constants.MOTOROLA_ANSPRECHPARTNER,
            "Text Field IMP 19": Constants.MOTOROLA_EMAILADRESSE,
            "Text Field IMP 20": Constants.MOTOROLA_TEL,
            "Text Field IMP 28": Constants.MOTOROLA_LIEFERADRESSE,
            "Text Field IMP 9": (
                self.reparatur.artikel_modellnummer
                or self.device.eg_typ
                or ""
            ),
            "Text Field IMP 12": seriennummer,
            "Text Field IMP 13": (
                self.reparatur.option_features
                or "siehe rechts " "(Leistungsmerkmale Pager)"
            ),
            "Text Field IMP 21": self.reparatur.plombennummern or "",
            "Text Field IMP 22": defektbeschreibung,
        }

        # -------------------------------------------------
        # Symptome
        # -------------------------------------------------

        for symptom in self.reparatur.symptome:
            field_name = self.SYMPTOM_FIELDS.get(symptom)

            if field_name:
                fields[field_name] = "/Yes"

        # -------------------------------------------------
        # Zubehör
        # -------------------------------------------------

        ACCESSORY_FIELDS = {
            "Batterie": "C3",
            "Antenne": "C4",
            "Bedienteil": "C5",
            "Trageclip": "C6",
            "Mikrofon": "C7",
            "Kopfhörer": "C8",
        }

        sonstiges = ""

        for zubehoer in self.reparatur.zubehoer:
            field_name = ACCESSORY_FIELDS.get(zubehoer)

            if field_name:
                fields[field_name] = "/Yes"
            elif zubehoer.strip():
                sonstiges = zubehoer.strip()

        fields["Text Field IMP 31"] = sonstiges

        # -------------------------------------------------
        # Reparaturart
        # -------------------------------------------------

        reparaturarten = self.reparatur.reparaturart

        if reparaturarten:
            reparaturart = reparaturarten[0]

            state = self.REPAIR_TYPE_STATES.get(
                reparaturart
            )

            if state:
                fields["R99"] = state

        # -------------------------------------------------
        # Formularwerte schreiben
        # -------------------------------------------------

        for page in writer.pages:
            writer.update_page_form_field_values(
                page,
                fields,
                auto_regenerate=False,
            )

        # -------------------------------------------------
        # PDF speichern
        # -------------------------------------------------

        with open(output_path, "wb") as pdf_file:
            writer.write(pdf_file)

        return output_path
