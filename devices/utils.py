import re
from datetime import date


def create_export_filename(organisationsname):

    name = organisationsname.lower().strip()

    replacements = {
        "ä": "ae",
        "ö": "oe",
        "ü": "ue",
        "ß": "ss",
    }

    for old, new in replacements.items():
        name = name.replace(old, new)

    name = re.sub(r"\s+", "_", name)
    name = re.sub(r"[^a-z0-9_]", "", name)

    return (
        f"import_tactilon_{name}_{date.today():%Y%m%d}.csv"
    )