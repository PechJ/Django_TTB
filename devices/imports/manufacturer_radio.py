import csv

from devices.models import Device
from .base import BaseImporter


class ManufacturerRadioImporter(BaseImporter):
    """
    Importiert Funk-Stammdaten aus der Sepura-Herstellerdatei.
    """

    COLUMN_TEI = "TEI"
    COLUMN_PRODUCT = "Produktname"
    COLUMN_SOFTWARE = "Aktuelle Version der Hauptsoftware"

    def run(self):

        # UTF-8 mit BOM lesen
        content = self.file.read().decode("utf-8-sig")

        # Zwei Informationszeilen überspringen
        lines = content.splitlines()[2:]

        reader = csv.DictReader(lines, delimiter=",")

        for row in reader:

            tei = row[self.COLUMN_TEI].strip()

            if not tei:
                self.result.skipped += 1
                continue

            product_name = row[self.COLUMN_PRODUCT].strip()
            software_version = row[self.COLUMN_SOFTWARE].strip()

            _, created = Device.objects.update_or_create(
                tei=tei,
                defaults={
                    "geraetename": product_name,
                    "softwareversion": software_version,
                },
            )

            if created:
                self.result.created += 1
            else:
                self.result.updated += 1

        return self.result