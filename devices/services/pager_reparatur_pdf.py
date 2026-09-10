from pathlib import Path

from pypdf import PdfReader, PdfWriter

from devices.constants import DeviceConstants as Constants


class PagerReparaturPdfGenerator:

    TEMPLATE_NAME = "02. Reparaturauftragsformular- Pager-.pdf"

    def __init__(self, reparatur):
        self.reparatur = reparatur
        self.device = reparatur.pager

    def generate(self):
        """
        Erstellt das ausgefüllte Motorola-Reparaturformular
        und speichert es im Downloads-Ordner.
        """

        # -------------------------------------------------
        # Vorlage
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
        # Downloads-Ordner
        # -------------------------------------------------

        downloads = Path.home() / "Downloads"
        downloads.mkdir(parents=True, exist_ok=True)

        # -------------------------------------------------
        # Seriennummer
        # -------------------------------------------------

        seriennummer = (self.device.seriennummer or "").strip()

        if not seriennummer:
            raise ValueError(
                "Der Pager besitzt keine Seriennummer."
            )

        filename = (
            f"02. Reparaturauftragsformular- Pager-"
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
        # Reparaturdaten
        # -------------------------------------------------

        symptome = self.reparatur.symptome or []
        reparaturart = self.reparatur.reparaturart or []
        zubehoer = self.reparatur.zubehoer or []

        # -------------------------------------------------
        # Formularfelder
        # -------------------------------------------------

        fields = {
            # Kunde
            "IMP 3": Constants.MOTOROLA_KUNDENNUMMER,
            "IMP 5": Constants.MOTOROLA_FIRMA,
            "IMP 8": Constants.MOTOROLA_ORGANISATION,
            "IMP 7": Constants.MOTOROLA_LIEFERADRESSE,

            # Lieferadresse Ansprechpartner
            "IMP 15": Constants.MOTOROLA_ANSPRECHPARTNER,
            "IMP 16": Constants.MOTOROLA_EMAILADRESSE,
            "IMP 17": Constants.MOTOROLA_TEL,

            # Rechnungsadresse
            "IMP 18": Constants.MOTOROLA_ANSPRECHPARTNER,
            "IMP 19": Constants.MOTOROLA_EMAILADRESSE,
            "IMP 20": Constants.MOTOROLA_TEL,
            "IMP 28": self.reparatur.rechnungsadresse,

            # Gerät
            "IMP 9": (
                self.reparatur.artikel_modellnummer
                or self.device.eg_typ
                or ""
            ),

            "IMP 12": seriennummer,

            "IMP 13": (
                self.reparatur.option_features
                or "siehe rechts (Leistungsmerkmale Pager)"
            ),

            # Plombennummern
            "IMP 21": self.reparatur.plombennummern or "",

            # Defektbeschreibung
            "IMP 22": self.reparatur.defektbeschreibung or "",
        }

        # -------------------------------------------------
        # Ansprechpartner / interne Bemerkung etc.
        # -------------------------------------------------
        #
        # Diese Felder werden bewusst noch nicht automatisch
        # befüllt, weil wir deren endgültige Bedeutung für
        # den vereinfachten Workflow noch nicht festgelegt
        # haben.
        #
        # -------------------------------------------------

        # -------------------------------------------------
        # Checkboxen / Auswahlfelder
        # -------------------------------------------------
        #
        # Die genaue Zuordnung der Acrobat-Choice-Felder
        # erfolgt separat anhand der gewünschten Werte.
        #
        # -------------------------------------------------

        # PDF-Felder setzen
        writer.update_page_form_field_values(
            writer.pages[0],
            fields,
            auto_regenerate=False,
        )

        # -------------------------------------------------
        # PDF speichern
        # -------------------------------------------------

        with open(output_path, "wb") as pdf_file:
            writer.write(pdf_file)

        return output_path