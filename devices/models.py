from django.db import models
from django.contrib.auth.models import User

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
    
    eg_art = models.CharField(
        max_length=10,
        blank=True,
        default="",
    )

    hersteller = models.CharField(
        max_length=100,
        blank=True,
        default="",
    )

    eg_typ = models.CharField(
        max_length=100,
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
    
    fahrzeugart = models.CharField(
        max_length=150,
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
    
    bemerkung = models.TextField(
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

    datum_ttb = models.DateTimeField(
        null=True,
        blank=True,
    )

    # ------------------------------------------------------------------
    # GOPTA / AOPTA
    # ------------------------------------------------------------------

    gopta_itsi = models.CharField(
        max_length=100,
        blank=True,
        default="",
    )

    aopta_land = models.CharField(
        max_length=20,
        blank=True,
        default="",
    )

    aopta_org = models.CharField(
        max_length=20,
        blank=True,
        default="",
    )

    aopta_region = models.CharField(
        max_length=20,
        blank=True,
        default="",
    )

    aopta_t = models.CharField(max_length=50, blank=True, default="")
    aopta_u = models.CharField(max_length=50, blank=True, default="")
    aopta_v = models.CharField(max_length=50, blank=True, default="")
    aopta_w = models.CharField(max_length=50, blank=True, default="")
    aopta_x = models.CharField(max_length=50, blank=True, default="")
    aopta_y = models.CharField(max_length=50, blank=True, default="")
    aopta_z = models.CharField(max_length=50, blank=True, default="")
    aopta_aa = models.CharField(max_length=50, blank=True, default="")
    aopta_ab = models.CharField(max_length=50, blank=True, default="")
    aopta_ac = models.CharField(max_length=50, blank=True, default="")
    aopta_ad = models.CharField(max_length=50, blank=True, default="")
    aopta_ae = models.CharField(max_length=50, blank=True, default="")
    aopta_af = models.CharField(max_length=50, blank=True, default="")
    aopta_ag = models.CharField(max_length=50, blank=True, default="")
    aopta_ah = models.CharField(max_length=50, blank=True, default="")
    aopta_ai = models.CharField(max_length=50, blank=True, default="")
    
    # ------------------------------------------------------------------
    # Status
    # ------------------------------------------------------------------
    
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.IN_BETRIEB,
    )
    
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    programming_date = models.DateTimeField(
        null=True,
        blank=True,
    )
    
    def __str__(self):
        return f"{self.geraetename} ({self.tei})"
    
    
class ImportStatus(models.Model):

    import_type = models.CharField(
        max_length=50,
        unique=True,
    )

    last_import = models.DateTimeField(
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.import_type}: {self.last_import}"