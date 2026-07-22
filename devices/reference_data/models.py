from dataclasses import dataclass

@dataclass(frozen=True)
class Gemeinde:
    name: str
    landkreis: str
    opta: str

@dataclass(frozen=True)
class Feuerwehr:
    name: str
    landkreis: str
    kommune: str
    dienststellenschluessel: str
