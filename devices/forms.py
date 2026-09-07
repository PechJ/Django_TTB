from django import forms


class ManufacturerRadioImportForm(forms.Form):
    file = forms.FileField(
        label="Seupra CSV-Datei"
    )


class PagerImportForm(forms.Form):

    file = forms.FileField(
        label="Pager CSV-Datei",
        required=True,
    )
        

class ImportForm(forms.Form):

    file = forms.FileField(
        label="Importdatei",
        required=True,
    )