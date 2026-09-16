from devices.constants import Landkreise, Organisationsarten, ValidationRules
from devices.reference_data import get_gemeinde
from devices.imports.excel_reader import ImportType


REQUIRED_FIELDS_ENDGERAETE = (
    "tei",
    "landkreis",
    "kommune",
    "organisationsart",
    "organisationsname",
    "funkrufname",
)

REQUIRED_FIELDS_SIRENEN = (
    "tei",
    "landkreis",
    "kommune",
    "organisationsart",
)


class InputValidator:
    """
    Validiert Eingabedaten vor dem Import.

    Der Validator schreibt niemals in die Datenbank.
    Er prüft ausschließlich die fachliche Gültigkeit der Eingabedaten.
    """

    def __init__(self, rows, import_type=ImportType.ENDGERAETE):
        self.rows = rows
        self.import_type = import_type
        self.errors = []

    def validate(self):

        self.validate_required_fields()
        self.validate_landkreis()
        self.validate_kommune()
        self.validate_organisationsart()
        self.validate_tei()

        if self.import_type == ImportType.ENDGERAETE:
            self.validate_opta()

        return self.errors

    def add_error(self, row, field, message):
        self.errors.append({
            "row": row,
            "field": field,
            "message": message,
        })

    def validate_required_fields(self):

        if self.import_type == ImportType.SIRENEN:
            required_fields = REQUIRED_FIELDS_SIRENEN
        else:
            required_fields = REQUIRED_FIELDS_ENDGERAETE

        for row_number, row in enumerate(self.rows, start=2):

            for field in required_fields:

                value = row.get(field, "").strip()

                if not value:
                    self.add_error(
                        row_number,
                        field,
                        "Pflichtfeld ist leer.",
                    )

    def validate_landkreis(self):

        for row_number, row in enumerate(self.rows, start=2):

            landkreis = row.get("landkreis", "").strip()

            if not landkreis:
                continue

            if landkreis not in Landkreise.ALL:
                self.add_error(
                    row_number,
                    "landkreis",
                    f"Ungültiger Landkreis: {landkreis}",
                )

    def validate_kommune(self):

        for row_number, row in enumerate(self.rows, start=2):

            landkreis = row.get("landkreis", "").strip()
            kommune = row.get("kommune", "").strip()

            if not landkreis or not kommune:
                continue

            gemeinde = get_gemeinde(
                landkreis,
                kommune,
            )

            if gemeinde is None:
                self.add_error(
                    row_number,
                    "kommune",
                    (
                        f"Kommune '{kommune}' "
                        f"existiert im Landkreis "
                        f"'{landkreis}' nicht."
                    ),
                )

    def validate_organisationsart(self):

        for row_number, row in enumerate(self.rows, start=2):

            organisationsart = row.get(
                "organisationsart",
                "",
            ).strip()

            if not organisationsart:
                continue

            if self.import_type == ImportType.SIRENEN:
                if organisationsart != "FW":
                    self.add_error(
                        row_number,
                        "organisationsart",
                        (
                            f"Ungültige Organisationsart "
                            f"für Sirene: {organisationsart}"
                        ),
                    )
                continue

            if organisationsart not in Organisationsarten.ALL:
                self.add_error(
                    row_number,
                    "organisationsart",
                    f"Ungültige Organisationsart: {organisationsart}",
                )

    def validate_tei(self):

        for row_number, row in enumerate(self.rows, start=2):

            tei = row.get("tei", "").strip()

            if not tei:
                continue

            if not tei.isdigit():
                self.add_error(
                    row_number,
                    "tei",
                    "TEI darf nur Ziffern enthalten.",
                )
                continue

            if len(tei) != ValidationRules.RADIO_TEI_LENGTH:
                self.add_error(
                    row_number,
                    "tei",
                    (
                        f"TEI muss genau "
                        f"{ValidationRules.RADIO_TEI_LENGTH} "
                        f"Ziffern enthalten."
                    ),
                )

    def validate_opta(self):

        for row_number, row in enumerate(self.rows, start=2):

            opta = row.get("opta", "").strip()
            kommune = row.get("kommune", "").strip()
            landkreis = row.get("landkreis", "").strip()

            gemeinde = get_gemeinde(
                landkreis,
                kommune,
            )

            if gemeinde is None:
                continue

            if opta != gemeinde.opta:
                self.add_error(
                    row_number,
                    "kommune",
                    (
                        f"OPTA '{opta}' stimmt nicht "
                        f"mit der Referenz "
                        f"'{gemeinde.opta}' überein."
                    ),
                )