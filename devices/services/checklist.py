from devices.models import Checkliste, Checklistenpunkt


CHECKLISTENPUNKTE = [
    ("ILS_GESENDET", "An ILS gesendet?"),
    ("TACTILON_IMPORT", "Tactilon-Import durchgeführt?"),
    ("RADIOMANAGER_EINGELESEN", "RadioManager eingelesen bzw. Add-Inf. geändert?"),
    ("MASTER_KONTAKTLISTE", "RadioManager Master-Kontaktliste ergänzt?"),
    ("TELEFONBUCH", "RadioManager Telefonbuch ergänzt?"),
    ("PROGRAMMIERSTAPEL", "RadioManager Programmierstapel erstellt?"),
    ("FUNKGERAET_PROGRAMMIERT", "Funkgerät programmiert?"),
    ("FEUERWEHR_INFORMIERT", "Feuerwehr informiert?"),
    ("PERSOENLICHE_ABHOLUNG", "Persönliche Abholung?"),
    ("POSTVERSAND_GESPERRT", "Gesperrt für Postversand?"),
    ("POSTVERSAND_ENTSPERRT", "Entsperrt nach Bestätigung?"),
    ("DFM_IMPORT", "DFM-Import durchgeführt?"),
]


def create_checklist(device, import_date):
    """
    Erstellt für einen erfolgreichen Lebend-Daten-Import
    eine neue Checkliste mit allen definierten Punkten.
    """

    checkliste = Checkliste.objects.create(
        geraet=device,
        import_am=import_date,
    )

    Checklistenpunkt.objects.bulk_create(
        [
            Checklistenpunkt(
                checkliste=checkliste,
                code=code,
                bezeichnung=bezeichnung,
                erforderlich=True,
            )
            for code, bezeichnung in CHECKLISTENPUNKTE
        ]
    )

    return checkliste