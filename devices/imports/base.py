from .result import ImportResult


class BaseImporter:
    """
    Basisklasse für alle zukünftigen Importer.
    """

    def __init__(self, file):
        self.file = file
        self.result = ImportResult()

    def run(self):
        raise NotImplementedError(
            "Jeder Importer muss run() implementieren."
        )