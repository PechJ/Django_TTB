from devices.models import Device, SirenFRTStatus


class FertigmeldungImporter:

    def __init__(self, rows):
        self.rows = rows
        self.updated = 0
        self.not_found = 0

    def run(self):

        for row in self.rows:

            # -------------------------------------------------
            # Device anhand des eindeutigen Hersteller-Schlüssels
            # -------------------------------------------------

            if row["hersteller"] == "Haeusler":

                device = Device.objects.filter(
                    tei=row["tei"]
                ).first()

            elif row["hersteller"] == "Hoermann":

                device = Device.objects.filter(
                    issi=row["issi"]
                ).first()

            else:
                device = None

            print("FERTIGMELDUNG:", row)
            print("GEFUNDENES DEVICE:", device)

            if not device:
                self.not_found += 1
                continue

            # -------------------------------------------------
            # Zugehörigen FRT-Status suchen
            # -------------------------------------------------

            status = SirenFRTStatus.objects.filter(
                sirene__device=device
            ).first()

            print("GEFUNDENER FRT-STATUS:", status)

            if not status:
                self.not_found += 1
                continue

            # -------------------------------------------------
            # Fertigmeldung übernehmen
            # -------------------------------------------------

            status.status = SirenFRTStatus.Status.FERTIG
            status.fertigmeldedatum = row["fertigmeldedatum"]

            status.save(
                update_fields=[
                    "status",
                    "fertigmeldedatum",
                ]
            )

            self.updated += 1

        return self