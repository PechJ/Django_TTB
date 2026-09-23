from django.db import models


class SirenFRTAntrag(models.Model):

    suchkreisname = models.CharField(
        max_length=150,
        blank=True,
        default="",
    )

    ort = models.CharField(
        max_length=100,
        blank=True,
        default="",
    )

    plz = models.CharField(
        max_length=10,
        blank=True,
        default="",
    )

    strasse = models.CharField(
        max_length=150,
        blank=True,
        default="",
    )

    hausnummer = models.CharField(
        max_length=20,
        blank=True,
        default="",
    )

    breitengrad_grad = models.IntegerField(
        null=True,
        blank=True,
    )

    breitengrad_min = models.IntegerField(
        null=True,
        blank=True,
    )

    breitengrad_sek = models.DecimalField(
        max_digits=8,
        decimal_places=3,
        null=True,
        blank=True,
    )

    laengengrad_grad = models.IntegerField(
        null=True,
        blank=True,
    )

    laengengrad_min = models.IntegerField(
        null=True,
        blank=True,
    )

    laengengrad_sek = models.DecimalField(
        max_digits=8,
        decimal_places=3,
        null=True,
        blank=True,
    )

    standorthoehe = models.CharField(
        max_length=20,
        blank=True,
        default="",
    )

    antragsdatum = models.DateTimeField(
        null=True,
        blank=True,
    )

    erstellt_am = models.DateTimeField(
        auto_now_add=True,
    )
    
    hersteller = models.CharField(
        max_length=100,
        blank=True,
        default="",
    )

    def __str__(self):
        return (
            f"FRT-Antrag – "
            f"{self.suchkreisname or self.strasse}"
        )
        
        
class SirenFRTFreigabePending(models.Model):
    suchkreisname = models.CharField(
        max_length=150,
        blank=True,
        default="",
    )

    freigabedatum = models.DateTimeField(
        null=True,
        blank=True,
    )

    as_kommentar = models.TextField(
        blank=True,
        default="",
    )

    zuteilungsnummer = models.CharField(
        max_length=150,
        blank=True,
        default="",
    )

    erstellt_am = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return (
            f"FRT-Freigabe wartet – "
            f"{self.suchkreisname}"
        )