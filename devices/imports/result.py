from dataclasses import dataclass, field


@dataclass
class ImportResult:
    """
    Ergebnis eines Imports.
    Jeder Importer gibt genau dieses Objekt zurück.
    """

    created: int = 0
    updated: int = 0
    skipped: int = 0

    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    @property
    def successful(self) -> bool:
        return not self.errors