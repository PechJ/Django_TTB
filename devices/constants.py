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