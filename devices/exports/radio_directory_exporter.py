from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment
from openpyxl.utils import get_column_letter
from devices.constants import DeviceConstants as Constants
from devices.models import Device, ImportStatus
from pathlib import Path


class RadioDirectoryExporter:

    MRT = "MRT"
    FRT = "FRT"

    DOWNLOAD_FOLDER = Path.home() / "Downloads"

    def __init__(self, landkreis):

        self.landkreis = landkreis

        status = ImportStatus.objects.get(
            import_type="endgeraete"
        )

        self.import_date = status.last_import.replace(
            tzinfo=None
        )

    def export(self):

        devices = Device.objects.filter(
            landkreis=self.landkreis
        )

        self.DOWNLOAD_FOLDER.mkdir(
            parents=True,
            exist_ok=True,
        )

        filename = (
            f"{self.import_date:%Y-%m-%d}"
            f"_Funkverzeichnis_Digitalfunk_"
            f"{self.landkreis}.xlsx"
        )

        filepath = self.DOWNLOAD_FOLDER / filename

        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "Datenimport"

        self._create_header(sheet)
        self._write_devices(sheet, devices)
        self._format_sheet(sheet)

        workbook.save(filepath)

        return filepath

    # ---------------------------------------------------------
    # HEADER
    # ---------------------------------------------------------

    def _create_header(self, sheet):

        headers = {
            "A1": "Datum        TTB",
            "B1": "Datum        ILS",
            "C1": "EG-Art",
            "D1": "Hersteller",
            "E1": "EG-Typ",
            "F1": "Seriennummer",
            "G1": "TEI",
            "H1": "MCC",
            "I1": "MNC",
            "J1": "SSI",
            "K1": "BOS-SiKa-Nummer",
            "L1": "BOS-SiKa-Name",
            "M1": "Fahrzeugart/Standort",
            "N1": "Funkrufname des Fahrzeugs/Standorts     max 32 Zeichen!",
            "O1": "Verwendung",
            "P1": "GOPTA-ITSI",
            "Q1": "AOPTA-Land",
            "R1": "AOPTA-Org",
            "S1": "AOPTA-Region",
            "T1": "AOPTA-Zusatz",
            "AJ1": "Bemerkung",
        }

        for cell, value in headers.items():
            sheet[cell] = value

        # A bis S über vier Zeilen
        for column in range(1, 20):
            letter = get_column_letter(column)

            sheet.merge_cells(
                f"{letter}1:{letter}4"
            )

        # AOPTA-Zusatz
        sheet.merge_cells("T1:AI1")

        # Bemerkung
        sheet.merge_cells("AJ1:AJ4")

        # AOPTA-Zusatz zweite Ebene
        for column, value in enumerate(
            range(9, 25),
            start=20,
        ):
            sheet.cell(
                row=2,
                column=column,
                value=value,
            )

        # AOPTA-Zusatz vierte Ebene
        sheet.merge_cells("T4:X4")
        sheet["T4"] = "4.1"

        sheet.merge_cells("Y4:AF4")
        sheet["Y4"] = "4.2"

        sheet.merge_cells("AG4:AH4")
        sheet["AG4"] = "4.3"

        sheet["AI4"] = 5

    # ---------------------------------------------------------
    # GERÄTEDATEN
    # ---------------------------------------------------------

    def _write_devices(self, sheet, devices):

        start_row = 5

        for row_number, device in enumerate(
            devices,
            start=start_row,
        ):

            sheet[f"A{row_number}"] = self.import_date

            sheet[f"B{row_number}"] = self._get(
                device,
                "datum_ils",
            )

            sheet[f"C{row_number}"] = self._get(
                device,
                "eg_art",
            )

            sheet[f"D{row_number}"] = self._get(
                device,
                "hersteller",
            )

            sheet[f"E{row_number}"] = self._get(
                device,
                "eg_typ",
            )

            sheet[f"F{row_number}"] = self._get(
                device,
                "seriennummer",
            )

            sheet[f"G{row_number}"] = self._get(
                device,
                "tei",
            )

            # Globale Konstanten
            sheet[f"H{row_number}"] = Constants.MCC
            sheet[f"I{row_number}"] = Constants.MNC

            sheet[f"J{row_number}"] = self._get(
                device,
                "issi",
            )

            sheet[f"K{row_number}"] = self._get(
                device,
                "sika_nummer",
                "sika-nummer",
            )

            sheet[f"L{row_number}"] = self._get(
                device,
                "sika_name",
                "sika-name",
            )

            sheet[f"M{row_number}"] = self._get(
                device,
                "fahrzeug",
            )

            sheet[f"N{row_number}"] = self._get(
                device,
                "funkrufname",
            )

            sheet[f"O{row_number}"] = self._get(
                device,
                "verwendung",
            )

            sheet[f"P{row_number}"] = self._get(
                device,
                "gopta_itsi",
            )

            sheet[f"Q{row_number}"] = self._get(
                device,
                "aopta_land",
            )

            sheet[f"R{row_number}"] = self._get(
                device,
                "aopta_org",
            )

            sheet[f"S{row_number}"] = self._get(
                device,
                "aopta_region",
            )

            # AOPTA-Zusatz
            for column in range(20, 36):

                letter = get_column_letter(column)

                value = self._get(
                    device,
                    f"aopta_{letter.lower()}",
                )

                sheet[
                    f"{letter}{row_number}"
                ] = value

            # Bemerkung
            sheet[f"AJ{row_number}"] = self._get(
                device,
                "bemerkung",
            )

            self._apply_row_style(
                sheet,
                row_number,
                self._get(
                    device,
                    "eg_art",
                ),
            )

    # ---------------------------------------------------------
    # ZEILENSTYLES
    # ---------------------------------------------------------

    def _apply_row_style(
        self,
        sheet,
        row_number,
        eg_art,
    ):

        if eg_art == self.MRT:

            self._apply_mrt_style(
                sheet,
                row_number,
            )

        elif eg_art == self.FRT:

            self._apply_frt_style(
                sheet,
                row_number,
            )

    def _apply_mrt_style(
        self,
        sheet,
        row_number,
    ):

        # Farbe wird noch exakt
        # aus der Originaldatei übernommen.

        pass

    def _apply_frt_style(
        self,
        sheet,
        row_number,
    ):

        # Farbe wird noch exakt
        # aus der Originaldatei übernommen.

        pass

    # ---------------------------------------------------------
    # FORMATIERUNG
    # ---------------------------------------------------------

    def _format_sheet(self, sheet):

        thin_side = Side(
            style="thin",
            color="000000",
        )

        border = Border(
            left=thin_side,
            right=thin_side,
            top=thin_side,
            bottom=thin_side,
        )

        for row in sheet.iter_rows(
            min_row=1,
            max_row=sheet.max_row,
            min_col=1,
            max_col=36,
        ):

            for cell in row:

                cell.font = Font(
                    name="Arial",
                    size=10,
                )

                cell.alignment = Alignment(
                    horizontal="left",
                    vertical="center",
                    wrap_text=True,
                )

                cell.border = border

        # Kopf fett und zentriert
        for row in sheet.iter_rows(
            min_row=1,
            max_row=4,
            min_col=1,
            max_col=36,
        ):

            for cell in row:

                cell.font = Font(
                    name="Arial",
                    size=10,
                    bold=True,
                )

                cell.alignment = Alignment(
                    horizontal="center",
                    vertical="center",
                    wrap_text=True,
                )

        # Datum
        for row in range(
            5,
            sheet.max_row + 1,
        ):

            sheet[
                f"A{row}"
            ].number_format = "DD.MM.YYYY"

        # Spaltenbreiten
        widths = {
            "A": 14,
            "B": 14,
            "C": 10,
            "D": 18,
            "E": 18,
            "F": 18,
            "G": 16,
            "H": 10,
            "I": 10,
            "J": 16,
            "K": 18,
            "L": 22,
            "M": 22,
            "N": 35,
            "O": 20,
            "P": 18,
            "Q": 12,
            "R": 12,
            "S": 14,
            "AJ": 40,
        }

        for column, width in widths.items():

            sheet.column_dimensions[
                column
            ].width = width

        for column in range(20, 36):

            letter = get_column_letter(column)

            sheet.column_dimensions[
                letter
            ].width = 10

        sheet.freeze_panes = "A5"

    # ---------------------------------------------------------
    # HILFSMETHODE
    # ---------------------------------------------------------

    def _get(self, device, *names):

        for name in names:

            value = getattr(
                device,
                name,
                None,
            )

            if value is not None:
                return value

        return ""
