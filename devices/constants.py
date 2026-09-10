class Landkreise:
    A = "A"
    AIC = "AIC"
    A_HASH = "A#"
    DLG = "DLG"
    DON = "DON"

    ALL = (
        A,
        AIC,
        A_HASH,
        DLG,
        DON,
    )


class Organisationsarten:
    FF = "FF"
    BF = "BF"
    WF = "WF"

    ALL = (
        FF,
        BF,
        WF,
    )
    

class ValidationRules:

    RADIO_TEI_LENGTH = 15
    
class DeviceConstants:
    REQUIRED_FIRMWARE = "V10.26 / SC 3.1"
    MCC = 262
    MNC = 1001

    # Motorola Reparaturformular
    MOTOROLA_KUNDENNUMMER = "3010256270"
    MOTOROLA_ANSPRECHPARTNER = "Jürgen Pech"
    MOTOROLA_FIRMA = "TTB Augsburg"
    MOTOROLA_ORGANISATION = "TTB Augsburg"

    MOTOROLA_LIEFERADRESSE = "Berliner Allee 30, 86153 Augsburg, Deutschland"

    MOTOROLA_RECHNUNGSADRESSE = "Berliner Allee 30, 86153 Augsburg, Deutschland"
    MOTOROLA_EMAILADRESSE = "Juergen.Pech@Augsburg.de"
    MOTOROLA_TEL = "0821 / 324 37 151"