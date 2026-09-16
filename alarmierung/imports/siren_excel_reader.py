from openpyxl import load_workbook


class SirenExcelReader:

    SHEET_NAME = "FRT_Import_Netsite_Pega"
    DATA_START_ROW = 13

    def __init__(self, uploaded_file):
        self.uploaded_file = uploaded_file

    def read(self):
        workbook = load_workbook(
            self.uploaded_file,
            data_only=True,
        )

        if self.SHEET_NAME not in workbook.sheetnames:
            raise ValueError(
                f"Tabellenblatt '{self.SHEET_NAME}' nicht gefunden."
            )

        sheet = workbook[self.SHEET_NAME]

        rows = []

        for excel_row in sheet.iter_rows(
            min_row=self.DATA_START_ROW,
            values_only=True,
        ):
            # Eine leere Zeile beendet den Datenbereich.
            if not any(
                value is not None
                for value in excel_row
            ):
                break

            # Wir interessieren uns nur für FRT.
            if str(excel_row[2]).strip() != "FRT":
                continue

            row = {
                "land": self._text(excel_row[1]),
                "endgeraetetyp": self._text(excel_row[2]),
                "suchkreisname": self._text(excel_row[3]),

                "breitengrad_grad": excel_row[4],
                "breitengrad_min": excel_row[5],
                "breitengrad_sek": excel_row[6],

                "laengengrad_grad": excel_row[7],
                "laengengrad_min": excel_row[8],
                "laengengrad_sek": excel_row[9],

                "standorthoehe": excel_row[10],

                "standortschluessel": self._text(
                    excel_row[11]
                ),

                "bemerkung_standort": self._text(
                    excel_row[12]
                ),

                "taktische_zuordnung_frt": self._text(
                    excel_row[13]
                ),

                "itsi_nummer": self._text(
                    excel_row[14]
                ),

                "ort": self._text(
                    excel_row[15]
                ),

                "plz": self._text(
                    excel_row[16]
                ),

                "strasse": self._text(
                    excel_row[17]
                ),

                "hausnummer": self._text(
                    excel_row[18]
                ),

                "neschluessel": self._text(
                    excel_row[19]
                ),

                "status": self._text(
                    excel_row[20]
                ),

                "tetra": self._text(
                    excel_row[21]
                ),

                "ausgangsleistung": excel_row[22],

                "antennentyp": self._text(
                    excel_row[23]
                ),

                "antennengewinn": excel_row[24],

                "anbindungs_tbs": self._text(
                    excel_row[35]
                ),

                "netzelementnummer_tbs": self._text(
                    excel_row[36]
                ),

                "stob_nr": self._text(
                    excel_row[40]
                ),

                "stob_datum": excel_row[41],

                "betreiber_funkanlage": self._text(
                    excel_row[42]
                ),

                "datum_inbetrieb": excel_row[43],

                "datum_ausbetrieb": excel_row[44],

                "bnetza_ast": self._text(
                    excel_row[45]
                ),

                "anmeldung_aenderung_abmeldung": self._text(
                    excel_row[49]
                ),

                "datum_an_abmeldung": excel_row[50],

                "antragsdatum": excel_row[51],
            }

            rows.append(row)

        return rows

    @staticmethod
    def _text(value):
        if value is None:
            return ""

        return str(value).strip()