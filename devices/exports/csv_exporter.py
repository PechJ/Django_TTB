import csv
from pathlib import Path


class CsvExporter:

    DOWNLOAD_FOLDER = Path.home() / "Downloads"

    def __init__(
        self,
        headers,
        rows,
        delimiter=";"
    ):

        self.headers = headers
        self.rows = rows
        self.delimiter = delimiter

    def export(self, filename):

        download_folder = self.DOWNLOAD_FOLDER

        download_folder.mkdir(
            parents=True,
            exist_ok=True,
        )

        filepath = download_folder / filename

        with open(
            filepath,
            "w",
            newline="",
            encoding="utf-8-sig",
        ) as csv_file:

            writer = csv.writer(
                csv_file,
                delimiter=self.delimiter,
            )

            writer.writerow(self.headers)
            writer.writerows(self.rows)

        return filepath
        
        