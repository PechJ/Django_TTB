from devices.models import Device, SirenStammdaten
from django.utils import timezone
from alarmierung.imports.siren_importer import pending_siren


class SirenImporter:

    def __init__(self, rows):
        self.rows = rows
        self.created = 0
        self.updated = 0

    def run(self):

        import_date = timezone.now()

        for row in self.rows:

            device, created = Device.objects.update_or_create(
                tei=row["tei"],
                defaults={
                    "datum_ttb": import_date,
                    "eg_art": row["eg_art"],
                    "hersteller": row["hersteller"],
                    "eg_typ": row["eg_typ"],
                    "landkreis": row["landkreis"],
                    "kommune": row["kommune"],
                    "organisationsart": row["organisationsart"],
                    "organisationsname": row["organisationsname"],
                    "seriennummer": row["seriennummer"],
                    "issi": row["issi"],
                    "bos_sika_nummer": row["sika-nummer"],
                    "bos_sika_name": row["sika-name"],
                },
            )

            siren_daten = row["siren_stammdaten"]

            SirenStammdaten.objects.update_or_create(
                device=device,
                defaults={
                    "gemeinde": siren_daten["gemeinde"],
                    "ortsteil": siren_daten["ortsteil"],
                    "standort_adresse": siren_daten["standort_adresse"],
                    "laufende_nummer": siren_daten["laufende_nummer"],
                    "feueralarm": siren_daten["feueralarm"],
                    "warnung": siren_daten["warnung"],
                    "sirenenprobe": siren_daten["sirenenprobe"],
                },
            )

            if created:
                self.created += 1
            else:
                self.updated += 1
                
        pending_siren()
        return self