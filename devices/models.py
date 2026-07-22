from django.db import models


class Device(models.Model):

    class Status(models.TextChoices):
        IN_BETRIEB = "betrieb", "In Betrieb"
        IN_REPARATUR = "reparatur", "In Reparatur"
        AUSGEMUSTERT = "archiv", "Ausgemustert"

    # ------------------------------------------------------------------
    # Herstellerdaten
    # ------------------------------------------------------------------

    tei = models.CharField(
        max_length=20,
        unique=True,
    )

    seriennummer = models.CharField(
        max_length=50,
        blank=True,
        default="",
    )

    geraetename = models.CharField(
        max_length=100,
        blank=True,
        default="",
    )

    software_version = models.CharField(
        max_length=50,
        blank=True,
        default="",
    )

    # ------------------------------------------------------------------
    # Funkdaten
    # ------------------------------------------------------------------

    issi = models.CharField(
        max_length=20,
        blank=True,
        default="",
    )

    bos_sika_nummer = models.CharField(
        max_length=50,
        blank=True,
        default="",
    )

    bos_sika_name = models.CharField(
        max_length=100,
        blank=True,
        default="",
    )

    # ------------------------------------------------------------------
    # Organisationsdaten
    # ------------------------------------------------------------------

    landkreis = models.CharField(
        max_length=5,
        blank=True,
        default="",
    )

    verwaltungsgemeinschaft = models.CharField(
        max_length=100,
        blank=True,
        default="",
    )

    kommune = models.CharField(
        max_length=100,
        blank=True,
        default="",
    )

    organisationsart = models.CharField(
        max_length=50,
        blank=True,
        default="",
    )

    organisationsname = models.CharField(
        max_length=150,
        blank=True,
        default="",
    )

    eigentuemer = models.CharField(
        max_length=150,
        blank=True,
        default="",
    )

    nutzer = models.CharField(
        max_length=150,
        blank=True,
        default="",
    )

    # ------------------------------------------------------------------
    # Verwendung
    # ------------------------------------------------------------------

    funkrufname = models.CharField(
        max_length=100,
        blank=True,
        default="",
    )

    verwendung = models.CharField(
        max_length=150,
        blank=True,
        default="",
    )

    # ------------------------------------------------------------------
    # Status
    # ------------------------------------------------------------------

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.IN_BETRIEB,
    )

    def __str__(self):
        return f"{self.geraetename} ({self.tei})"