class TactilonRadioBuilder:

    HEADERS = [
        "mcc",
        "mnc",
        "ssi",
        "primaryProfile",
        "activeProfileIndex",
        "organisation",
        "mnemonic",
        "ipAddressTypeSelection",
        "supportOverTheAirEnabling",
        "markingIndex",
        "unpaidBill",
        "stolenLost",
        "other",
        "smartCard",
        "comment",
    ]
    
    ORGANISATIONS = {
                            "AIC": "123-12-1-1",
                            "A":   "123-12-1-2",
                            "A#":  "123-12-1-3",
                            "DLG": "123-12-1-4",
                            "DON": "123-12-1-5",
                            }

    def __init__(self, rows):

        self.rows = rows

    def build(self):

        export_rows = []

        for row in self.rows:

            export_rows.append(
                self._build_row(row)
            )

        return self.HEADERS, export_rows

    def _build_row(self, row):

        return [

                "262",

                "1001",

                row["issi"],

                "1423112",

                "1",

                self._organisation(row),

                self._mnemonic(row),

                "2",

                "1",

                "1",

                "0",

                "0",

                "0",

                "",

                self._comment(row),

                ]
        
    def _organisation(self, row):
        
        return self.ORGANISATIONS[row["landkreis"]]
        
        
    def _mnemonic(self, row):

        organisationsart = row["organisationsart"]
        landkreis = row["landkreis"]
        issi = row["issi"]
        name = row["organisationsname"]

        if organisationsart == "BF":
            return f"BF_{landkreis}_{issi}"

        if organisationsart == "WF":
            return f"WF_{name}"

        return f"FW_{landkreis}_{issi}"

    def _comment(self, row):

        organisationsart = row["organisationsart"]
        landkreis = row["landkreis"]
        name = row["organisationsname"]

        if organisationsart == "BF":
            return f"BF_{landkreis}"

        if organisationsart == "WF":
            return f"WF_{name}"

        return f"FF_{name}_{landkreis}"