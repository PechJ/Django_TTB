from devices.models import Device


class DeviceImporter:

    def __init__(self, rows):
        self.rows = rows

        self.created = 0
        self.updated = 0
        self.skipped = 0

    def run(self):

        for row in self.rows:

            device, created = Device.objects.update_or_create(
                tei=row["tei"],
                defaults={
                    "landkreis": row["landkreis"],
                    "kommune": row["kommune"],
                    "organisationsart": row["organisationsart"],
                    "organisationsname": row["organisationsname"],
                    "funkrufname": row["funkrufname"],
                    "opta": row["opta"],
                    "seriennummer": row["seriennummer"],
                    "sika-nummer": row["sika-nummer"],
                    "sika-name": row["sika-name"],
                    "issi": row["issi"],
                },
            )
            
            if created:
                self.created += 1
            else:
                self.updated += 1

        return self