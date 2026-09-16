from alarmierung.models import SirenFRTAntrag


def normalisiere_adresse(adresse):
    if not adresse:
        return ""

    adresse = adresse.lower().strip()

    # Unterschiedliche Schreibweisen von Straße vereinheitlichen
    adresse = adresse.replace("straße", "strasse")
    adresse = adresse.replace("str.", "strasse")
    adresse = adresse.replace("strasse", "strasse")

    # ß generell vereinheitlichen
    adresse = adresse.replace("ß", "ss")

    # Mehrfache Leerzeichen entfernen
    adresse = " ".join(adresse.split())

    return adresse


class SirenFRTAntragImporter:

    def __init__(self, rows):
        self.rows = rows
        self.created = 0

    def run(self):
        for row in self.rows:
            SirenFRTAntrag.objects.create(
                suchkreisname=row["suchkreisname"],
                ort=row["ort"],
                plz=row["plz"],
                strasse=row["strasse"],
                hausnummer=row["hausnummer"],
                breitengrad_grad=row["breitengrad_grad"],
                breitengrad_min=row["breitengrad_min"],
                breitengrad_sek=row["breitengrad_sek"],
                laengengrad_grad=row["laengengrad_grad"],
                laengengrad_min=row["laengengrad_min"],
                laengengrad_sek=row["laengengrad_sek"],
                standorthoehe=row["standorthoehe"],
                antragsdatum=row["antragsdatum"],
            )

            self.created += 1

        return self