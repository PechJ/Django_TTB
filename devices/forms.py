from django import forms


class ManufacturerRadioImportForm(forms.Form):
    file = forms.FileField(
        label="Selectric CSV-Datei"
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
    
    
class ManufacturerForm(forms.Form):

    hersteller = forms.ChoiceField(
        label="Hersteller",
        choices=[
            ("Haeusler", "Häusler"),
            ("Hoermann", "Hörmann"),
        ],
        required=True,
    )