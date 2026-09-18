from alarmierung.models import SirenFRTAntrag
from devices.models import SirenStammdaten, SirenFRTStatus


def normalisiere_adresse(adresse):
    if not adresse:
        return ""

    adresse = adresse.lower().strip()

    adresse = adresse.replace("straße", "strasse")
    adresse = adresse.replace("str.", "strasse")
    adresse = adresse.replace("ß", "ss")

    adresse = " ".join(adresse.split())

    return adresse


def finde_sirene(antrag):
    gesuchte_adresse = normalisiere_adresse(
        f"{antrag.strasse} {antrag.hausnummer}"
    )

    gesuchter_ort = normalisiere_adresse(
        antrag.ort
    )

    treffer = []

    for sirene in SirenStammdaten.objects.all():

        vorhandene_adresse = normalisiere_adresse(
            sirene.standort_adresse
        )

        vorhandene_gemeinde = normalisiere_adresse(
            sirene.gemeinde
        )

        vorhandener_ortsteil = normalisiere_adresse(
            sirene.ortsteil
        )

        ort_passt = (
            gesuchter_ort == vorhandene_gemeinde
            or gesuchter_ort == vorhandener_ortsteil
        )

        if (
            gesuchte_adresse == vorhandene_adresse
            and ort_passt
        ):
            treffer.append(sirene)

    return treffer


class SirenFRTAntragImporter:

    def __init__(self, rows):
        self.rows = rows
        self.created = 0
        self.status_created = 0
        self.waiting_created = 0

    def run(self):

        for row in self.rows:

            antrag = SirenFRTAntrag(
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

            sirenen = finde_sirene(antrag)

            if sirenen:

                sirene = sirenen[0]

                SirenFRTStatus.objects.update_or_create(
                    sirene=sirene,
                    defaults={
                        "status": SirenFRTStatus.Status.BEANTRAGT,
                        "antragsdatum": antrag.antragsdatum,
                        "suchkreisname": antrag.suchkreisname,
                    },
                )

                self.status_created += 1

            else:

                antrag.save()

                self.waiting_created += 1

            self.created += 1

        return self
    
    
class SirenFRTFreigabeImporter:

    def __init__(self, rows):
        self.rows = rows
        self.updated = 0
        self.not_found = 0

    def run(self):
        
        print(" SirenFRTFreigabeImporter WIRD AUFGERUFEN ")

        for row in self.rows:

            suchkreisname = row["suchkreisname"]
            
            print("FRT FREIGABE:", repr(suchkreisname))

            status = (
                SirenFRTStatus.objects
                .filter(
                    suchkreisname=suchkreisname
                )
                .first()
            )

            print("GEFUNDENER STATUS:", status)
            
            if not status:
                self.not_found += 1
                continue

            status.status = SirenFRTStatus.Status.FREIGEGEBEN
            status.freigabedatum = row["freigabedatum"]
            status.as_kommentar = row["as_kommentar"]

            status.save(
                update_fields=[
                    "status",
                    "freigabedatum",
                    "as_kommentar",
                ]
            )

            self.updated += 1

        return self