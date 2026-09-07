import csv

from .base import BaseImporter


class PagerImporter(BaseImporter):
    """
    Importiert Pager-Stammdaten aus der Motorola-Pager-CSV.

    TEI ist der eindeutige Schlüssel eines Pagers.
    """

    COLUMN_TEI = "TEI"
    COLUMN_ISSI = "ISSI"
    COLUMN_HEIMAT_DIENSTSTELLE = "Heimat-Dienststelle"
    COLUMN_PAGER_NAME = "Pager-Name"
    COLUMN_FIRMWARE = "Firmware-Version"

    HERSTELLER = "Motorola"
    EG_TYP = "TPG2200"

    def run(self):

        # Die Pager-CSV ist nicht UTF-8.
        content = self.file.read().decode("cp1252")

        reader = csv.DictReader(
            content.splitlines(),
            delimiter=";",
        )

        for row in reader:

            tei = row[self.COLUMN_TEI].strip()

            if not tei:
                self.result.skipped += 1
                continue

            issi = row[self.COLUMN_ISSI].strip()
            heimat_dienststelle = row[
                self.COLUMN_HEIMAT_DIENSTSTELLE
            ].strip()
            pager_name = row[
                self.COLUMN_PAGER_NAME
            ].strip()
            firmware = row[
                self.COLUMN_FIRMWARE
            ].strip()

            # ----------------------------------------------------------
            # Organisationsdaten aus Heimat-Dienststelle
            # ----------------------------------------------------------

            dienststelle = heimat_dienststelle
            landkreis = ""

            if " - " in heimat_dienststelle:
                dienststelle, landkreis = (
                    heimat_dienststelle.rsplit(" - ", 1)
                )

                dienststelle = dienststelle.strip()
                landkreis = landkreis.strip()

            # Eigentümer nur bei einem neuen Gerät setzen.
            #
            # Beispiel:
            # FF Pöttmes (Dst.) - Augsburg
            #
            # -> Eigentümer = Pöttmes
            #
            eigentuemer = ""

            if dienststelle:
                eigentuemer = dienststelle

                if eigentuemer.startswith("FF "):
                    eigentuemer = eigentuemer[3:]

                elif eigentuemer.startswith("BF "):
                    eigentuemer = eigentuemer[3:]

                elif eigentuemer.startswith("WF "):
                    eigentuemer = eigentuemer[3:]

                if " (Dst.)" in eigentuemer:
                    eigentuemer = eigentuemer.split(
                        " (Dst.)",
                        1,
                    )[0]

                eigentuemer = eigentuemer.strip()

            # ----------------------------------------------------------
            # Gerät anhand TEI suchen
            # ----------------------------------------------------------

            from devices.models import Device

            device = Device.objects.filter(
                tei=tei
            ).first()

            if device:

                # Bestehende Daten:
                # Seriennummer und Status NICHT verändern.
                #
                # Eigentümer ebenfalls NICHT verändern,
                # weil dieser später manuell geändert werden kann.

                device.issi = issi
                device.heimat_dienststelle = heimat_dienststelle
                device.dienststelle = dienststelle
                device.landkreis = landkreis
                device.geraetename = pager_name
                device.software_version = firmware

                device.hersteller = self.HERSTELLER
                device.eg_typ = self.EG_TYP

                device.save()

                self.result.updated += 1

            else:

                # Neuer Pager
                device = Device.objects.create(
                    tei=tei,
                    issi=issi,
                    heimat_dienststelle=heimat_dienststelle,
                    dienststelle=dienststelle,
                    landkreis=landkreis,
                    eigentuemer=eigentuemer,
                    geraetename=pager_name,
                    software_version=firmware,
                    hersteller=self.HERSTELLER,
                    eg_typ=self.EG_TYP,
                )

                self.result.created += 1

        return self.result