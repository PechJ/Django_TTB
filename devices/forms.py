from django import forms


class ManufacturerRadioImportForm(forms.Form):
    file = forms.FileField(
        label="Seupra CSV-Datei"
    )
    

class ImportForm(forms.Form):

    file = forms.FileField(
        label="Importdatei",
        required=True,
    )