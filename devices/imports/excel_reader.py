from openpyxl import load_workbook


class ExcelReader:

    def __init__(self, file):
        self.file = file

    def read(self):

        COLUMN_SERIALNUMBER = 4
        COLUMN_TEI = 5
        COLUMN_ISSI = 8
        COLUMN_SIKANUMBER = 9
        COLUMN_SIKANAME = 10
        COLUMN_UNIT = 11
        COLUMN_FUNKRUFNAME = 12
        COLUMN_USECASE = 13
        

        workbook = load_workbook(
            self.file,
            data_only=True,
        )

        sheet = workbook.active

        # Stammdaten aus dem Formular
        landkreis = sheet["D4"].value
        kommune = sheet["D6"].value
        organisationsart = sheet["D7"].value
        organisationsname = sheet["D8"].value

        rows = []

        # Gerätetabelle beginnt bei Zeile 18
        for excel_row in sheet.iter_rows(min_row=18, values_only=True):
            opta = "".join(
                str(excel_row[i]).strip()
                for i in range(18, 23)
                if excel_row[i]
            )
            opta2 = "".join(
                str(excel_row[i]).strip()
                for i in range(24, 34)
                if excel_row[i]
            )
            row = {
                "landkreis": str(landkreis).strip() if landkreis else "",
                "kommune": str(kommune).strip() if kommune else "",
                "organisationsart": str(organisationsart).strip() if organisationsart else "",
                "organisationsname": str(organisationsname).strip() if organisationsname else "",

                # Diese Spalten müssen wir ggf. noch anpassen,
                # sobald wir die exakten Spalten kennen.
                "seriennummer": str(excel_row[COLUMN_SERIALNUMBER]).strip() if excel_row[COLUMN_SERIALNUMBER] else "",
                "tei": str(excel_row[COLUMN_TEI]).strip() if excel_row[COLUMN_TEI] else "",
                "opta": opta,
                "issi": str(excel_row[COLUMN_ISSI]).strip() if excel_row[COLUMN_ISSI] else "",
                "sika-nummer": str(excel_row[COLUMN_SIKANUMBER]).strip() if excel_row[COLUMN_SIKANUMBER] else "",
                "sika-name": str(excel_row[COLUMN_SIKANAME]).strip() if excel_row[COLUMN_SIKANAME] else "",
                "fahrzeug": str(excel_row[COLUMN_UNIT]).strip() if excel_row[COLUMN_UNIT] else "",
                "funkrufname": str(excel_row[COLUMN_FUNKRUFNAME]).strip() if excel_row[COLUMN_FUNKRUFNAME] else "",
                "verwendung": str(excel_row[COLUMN_USECASE]).strip() if excel_row[COLUMN_USECASE] else "",
                "opta2": opta2
            }
            print(row)
            if not excel_row[5]:
                break

            rows.append(row)

        return rows