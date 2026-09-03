from devices.models import Device
from django.utils import timezone


class DeviceImporter:

    def __init__(self, rows):
        self.rows = rows

        self.created = 0
        self.updated = 0
        self.skipped = 0

    def run(self):
        
        import_date = timezone.now()
                
        for row in self.rows:

            device, created = Device.objects.update_or_create(
                tei=row["tei"],
                defaults={
                    "datum_ttb": import_date,
                    "eg_art": row["eg_art"],
                    "hersteller": row["hersteller"],
                    "landkreis": row["landkreis"],
                    "kommune": row["kommune"],
                    "organisationsart": row["organisationsart"],
                    "organisationsname": row["organisationsname"],
                    "funkrufname": row["funkrufname"],
                    "seriennummer": row["seriennummer"],
                    "bos_sika_nummer": row["sika-nummer"],
                    "bos_sika_name": row["sika-name"],
                    "fahrzeugart": row["fahrzeugart"],
                    "verwendung": row["verwendung"],
                    "issi": row["issi"],
                    "gopta_itsi": row["gopta_itsi"],
                    "aopta_land": row["aopta_land"],
                    "aopta_org": row["aopta_org"],
                    "aopta_region": row["aopta_region"],
                    "aopta_t": row["aopta_t"],
                    "aopta_u": row["aopta_u"],
                    "aopta_v": row["aopta_v"],
                    "aopta_w": row["aopta_w"],
                    "aopta_x": row["aopta_x"],
                    "aopta_y": row["aopta_y"],
                    "aopta_z": row["aopta_z"],
                    "aopta_aa": row["aopta_aa"],
                    "aopta_ab": row["aopta_ab"],
                    "aopta_ac": row["aopta_ac"],
                    "aopta_ad": row["aopta_ad"],
                    "aopta_ae": row["aopta_ae"],
                    "aopta_af": row["aopta_af"],
                    "aopta_ag": row["aopta_ag"],
                    "aopta_ah": row["aopta_ah"],
                    "aopta_ai": row["aopta_ai"],
                    },
                )
            
            if created:
                self.created += 1
            else:
                self.updated += 1

        return self