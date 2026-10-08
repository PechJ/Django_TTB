from openpyxl import Workbook
from pathlib import Path
from devices.models import Device


class DfmExporter:
    
    HEADERS = [
            "TEI *",
            "Hersteller (* bei Neuanlage)",
            "Gerätetyp (* bei Neuanlage)",
            "Geräteart *",
            "Betriebsstellen ID *",
            "Seriennummer",
            "Bemerkung",
            "Ansprechpartner",
            "Organisation",
            "Kfz-Kennzeichen",
            "Fahrzeug (Kurzzeichen)",
            "Bestellung",
            "Auftrag",
            "Lieferschein",
            "Lieferdatum",
            "Rechnung",
            "SNr-Bedienteil",
            "SNr-Bedienteil2",
            "Datum Ausgabe",
            "Datum Rückgabe",
            "Ausgabestatus",
            "Kaufdatum",
            "Garantieende",
            "Wartungsfirma",
            "PEI-Schnittstelle",
            "Prog.System EG-Name",
            "ISSI",
            "Funkrufname",
            "Sonstiges",
            "OPTA",
            ]
    
    datalist = [
                ["FF Adelzhausen","7","71","111","2","14","14FW77111102","Schwaben","AIC","Adelzhausen","771111"],
                ["FF Burgadelzhausen","7","71","111","1","14","14FW77111101","Schwaben","AIC","Adelzhausen","771111"],
                ["FF Heretshausen","7","71","111","2","14","14FW77111102","Schwaben","AIC","Adelzhausen","771111"],
                ["FF Affing","7","71","112","1","14","14FW77111201","Schwaben","AIC","Affing","771112"],
                ["FF Anwalting","7","71","112","2","14","14FW77111202","Schwaben","AIC","Affing","771112"],
                ["FF Aulzhausen","7","71","112","3","14","14FW77111203","Schwaben","AIC","Affing","771112"],
                ["FF Gebenhofen","7","71","112","4","14","14FW77111204","Schwaben","AIC","Affing","771112"],
                ["FF Haunswies","7","71","112","5","14","14FW77111205","Schwaben","AIC","Affing","771112"],
                ["FF Mühlhausen","7","71","112","6","14","14FW77111206","Schwaben","AIC","Affing","771112"],
                ["BtF JVA Aichach","7","71","113","1","14","14FW77111301","Schwaben","AIC","Aichach","771113"],
                ["FF Aichach","7","71","113","2","14","14FW77111302","Schwaben","AIC","Aichach","771113"],
                ["FF Ecknach","7","71","113","3","14","14FW77111303","Schwaben","AIC","Aichach","771113"],
                ["FF Edenried","7","71","113","4","14","14FW77111304","Schwaben","AIC","Aichach","771113"],
                ["FF Gallenbach","7","71","113","5","14","14FW77111305","Schwaben","AIC","Aichach","771113"],
                ["FF Griesbeckerzell","7","71","113","6","14","14FW77111306","Schwaben","AIC","Aichach","771113"],
                ["FF Klingen","7","71","113","7","14","14FW77111307","Schwaben","AIC","Aichach","771113"],
                ["FF Mauerbach","7","71","113","8","14","14FW77111308","Schwaben","AIC","Aichach","771113"],
                ["FF Oberbernbach","7","71","113","9","14","14FW77111309","Schwaben","AIC","Aichach","771113"],
                ["FF Oberschneitbach","7","71","113","10","14","14FW77111310","Schwaben","AIC","Aichach","771113"],
                ["FF Oberwittelsbach","7","71","113","11","14","14FW77111311","Schwaben","AIC","Aichach","771113"],
                ["FF Sulzbach","7","71","113","12","14","14FW77111312","Schwaben","AIC","Aichach","771113"],
                ["FF Unterwittelsbach","7","71","113","13","14","14FW77111313","Schwaben","AIC","Aichach","771113"],
                ["FF Walchshofen","7","71","113","14","14","14FW77111314","Schwaben","AIC","Aichach","771113"],
                ["FF Aindling","7","71","114","1","14","14FW77111401","Schwaben","AIC","Aindling","771114"],
                ["FF Pichl-Binnenbach","7","71","114","2","14","14FW77111402","Schwaben","AIC","Aindling","771114"],
                ["FF Stotzard","7","71","114","3","14","14FW77111403","Schwaben","AIC","Aindling","771114"],
                ["FF Baar","7","71","176","1","14","14FW77117601","Schwaben","AIC","Baar (Schwaben)","771176"],
                ["FF Dasing","7","71","122","1","14","14FW77112201","Schwaben","AIC","Dasing","771122"],
                ["FF Laimering","7","71","122","2","14","14FW77112202","Schwaben","AIC","Dasing","771122"],
                ["FF Rieden","7","71","122","3","14","14FW77112203","Schwaben","AIC","Dasing","771122"],
                ["FF Taiting-Bitzenhofen","7","71","122","4","14","14FW77112204","Schwaben","AIC","Dasing","771122"],
                ["FF Wessiszell","7","71","122","5","14","14FW77112205","Schwaben","AIC","Dasing","771122"],
                ["FF Eurasburg","7","71","129","1","14","14FW77112901","Schwaben","AIC","Eurasburg","771129"],
                ["FF Freienried","7","71","129","2","14","14FW77112902","Schwaben","AIC","Eurasburg","771129"],
                ["FF Bachern","7","71","130","1","14","14FW77113001","Schwaben","AIC","Friedberg","771130"],
                ["FF Derching","7","71","130","2","14","14FW77113002","Schwaben","AIC","Friedberg","771130"],
                ["FF Friedberg","7","71","130","3","14","14FW77113003","Schwaben","AIC","Friedberg","771130"],
                ["FF Haberskirch","7","71","130","4","14","14FW77113004","Schwaben","AIC","Friedberg","771130"],
                ["FF Hügelshart","7","71","130","5","14","14FW77113005","Schwaben","AIC","Friedberg","771130"],
                ["FF Ottmaring","7","71","130","6","14","14FW77113006","Schwaben","AIC","Friedberg","771130"],
                ["FF Paar-Harthausen","7","71","130","7","14","14FW77113007","Schwaben","AIC","Friedberg","771130"],
                ["FF Rederzhausen","7","71","130","8","14","14FW77113008","Schwaben","AIC","Friedberg","771130"],
                ["FF Rinnenthal","7","71","130","9","14","14FW77113009","Schwaben","AIC","Friedberg","771130"],
                ["FF Rohrbach","7","71","130","10","14","14FW77113010","Schwaben","AIC","Friedberg","771130"],
                ["FF Stätzling","7","71","130","11","14","14FW77113011","Schwaben","AIC","Friedberg","771130"],
                ["FF Wiffertshausen","7","71","130","12","14","14FW77113012","Schwaben","AIC","Friedberg","771130"],
                ["FF Wulfertshausen","7","71","130","13","14","14FW77113013","Schwaben","AIC","Friedberg","771130"],
                ["WF Federal Mogul GmbH Friedberg","7","71","130","14","14","14FW77113014","Schwaben","AIC","Friedberg","771130"],
                ["FF Hollenbach","7","71","140","1","14","14FW77114001","Schwaben","AIC","Hollenbach","771140"],
                ["FF Igenhausen","7","71","140","2","14","14FW77114002","Schwaben","AIC","Hollenbach","771140"],
                ["FF Mainbach","7","71","140","3","14","14FW77114003","Schwaben","AIC","Hollenbach","771140"],
                ["FF Motzenhofen","7","71","140","4","14","14FW77114004","Schwaben","AIC","Hollenbach","771140"],
                ["FF Schönbach","7","71","140","5","14","14FW77114005","Schwaben","AIC","Hollenbach","771140"],
                ["FF Inchenhofen","7","71","141","1","14","14FW77114101","Schwaben","AIC","Inchenhofen","771141"],
                ["FF Oberbachern","7","71","141","2","14","14FW77114102","Schwaben","AIC","Inchenhofen","771141"],
                ["FF Sainbach","7","71","141","3","14","14FW77114103","Schwaben","AIC","Inchenhofen","771141"],
                ["FF Kissing","7","71","142","1","14","14FW77114201","Schwaben","AIC","Kissing","771142"],
                ["FF Haslangkreit","7","71","144","1","14","14FW77114401","Schwaben","AIC","Kühbach","771144"],
                ["FF Kühbach","7","71","144","2","14","14FW77114402","Schwaben","AIC","Kühbach","771144"],
                ["FF Oberschönbach","7","71","144","3","14","14FW77114403","Schwaben","AIC","Kühbach","771144"],
                ["FF Stockensau","7","71","144","4","14","14FW77114404","Schwaben","AIC","Kühbach","771144"],
                ["FF Unterbernbach","7","71","144","5","14","14FW77114405","Schwaben","AIC","Kühbach","771144"],
                ["FF Hochdorf","7","71","145","1","14","14FW77114501","Schwaben","AIC","Merching","771145"],
                ["FF Merching","7","71","145","2","14","14FW77114502","Schwaben","AIC","Merching","771145"],
                ["FF Steinach","7","71","145","3","14","14FW77114503","Schwaben","AIC","Merching","771145"],
                ["FF Mering","7","71","146","1","14","14FW77114601","Schwaben","AIC","Mering","771146"],
                ["FF Baierberg","7","71","146","2","14","14FW77114602","Schwaben","AIC","Mering","771146"],
                ["FF Obergriesbach","7","71","149","1","14","14FW77114901","Schwaben","AIC","Obergriesbach","771149"],
                ["FF Zahling","7","71","149","2","14","14FW77114902","Schwaben","AIC","Obergriesbach","771149"],
                ["FF Alsmoos-Petersdorf","7","71","155","1","14","14FW77115501","Schwaben","AIC","Petersdorf","771155"],
                ["FF Willprechtszell-Schönleiten","7","71","155","2","14","14FW77115502","Schwaben","AIC","Petersdorf","771155"],
                ["FF Ebenried","7","71","156","1","14","14FW77115601","Schwaben","AIC","Pöttmes","771156"],
                ["FF Echsheim","7","71","156","2","14","14FW77115602","Schwaben","AIC","Pöttmes","771156"],
                ["FF Grimolzhausen","7","71","156","3","14","14FW77115603","Schwaben","AIC","Pöttmes","771156"],
                ["FF Gundelsdorf","7","71","156","4","14","14FW77115604","Schwaben","AIC","Pöttmes","771156"],
                ["FF Handzell","7","71","156","5","14","14FW77115605","Schwaben","AIC","Pöttmes","771156"],
                ["FF Kühnhausen","7","71","156","6","14","14FW77115606","Schwaben","AIC","Pöttmes","771156"],
                ["FF Osterzhausen","7","71","156","7","14","14FW77115607","Schwaben","AIC","Pöttmes","771156"],
                ["FF Pöttmes","7","71","156","8","14","14FW77115608","Schwaben","AIC","Pöttmes","771156"],
                ["FF Schnellmannskreuth","7","71","156","9","14","14FW77115609","Schwaben","AIC","Pöttmes","771156"],
                ["FF Schorn","7","71","156","10","14","14FW77115610","Schwaben","AIC","Pöttmes","771156"],
                ["FF Wiesenbach","7","71","156","11","14","14FW77115611","Schwaben","AIC","Pöttmes","771156"],
                ["FF Rehling","7","71","158","1","14","14FW77115801","Schwaben","AIC","Rehling","771158"],
                ["FF Baindlkirch","7","71","160","1","14","14FW77116001","Schwaben","AIC","Ried","771160"],
                ["FF Eismannsberg","7","71","160","2","14","14FW77116002","Schwaben","AIC","Ried","771160"],
                ["FF Hörmannsberg","7","71","160","3","14","14FW77116003","Schwaben","AIC","Ried","771160"],
                ["FF Ried","7","71","160","4","14","14FW77116004","Schwaben","AIC","Ried","771160"],
                ["FF Allenberg","7","71","162","1","14","14FW77116201","Schwaben","AIC","Schiltberg","771162"],
                ["FF Rapperzell","7","71","162","2","14","14FW77116202","Schwaben","AIC","Schiltberg","771162"],
                ["FF Ruppertszell","7","71","162","3","14","14FW77116203","Schwaben","AIC","Schiltberg","771162"],
                ["FF Schiltberg","7","71","162","4","14","14FW77116204","Schwaben","AIC","Schiltberg","771162"],
                ["FF Schmiechen","7","71","163","1","14","14FW77116301","Schwaben","AIC","Schmiechen","771163"],
                ["FF Unterbergen","7","71","163","2","14","14FW77116302","Schwaben","AIC","Schmiechen","771163"],
                ["FF Sielenbach","7","71","165","1","14","14FW77116501","Schwaben","AIC","Sielenbach","771165"],
                ["FF Tödtenried","7","71","165","2","14","14FW77116502","Schwaben","AIC","Sielenbach","771165"],
                ["FF Steindorf","7","71","168","1","14","14FW77116801","Schwaben","AIC","Steindorf","771168"],
                ["FF Eresried","7","71","168","2","14","14FW77116802","Schwaben","AIC","Steindorf","771168"],
                ["FF Hausen","7","71","168","3","14","14FW77116803","Schwaben","AIC","Steindorf","771168"],
                ["FF Hofhegnenberg","7","71","168","4","14","14FW77116804","Schwaben","AIC","Steindorf","771168"],
                ["FF Todtenweis","7","71","169","1","14","14FW77116901","Schwaben","AIC","Todtenweis","771169"],
                ["FF Adelsried","7","72","111","1","14","14FW77211101","Schwaben","A#","Adelsried","772111"],
                ["FF Allmannshofen","7","72","114","1","14","14FW77211401","Schwaben","A#","Allmannshofen","772114"],
                ["FF Altenmünster","7","72","115","1","14","14FW77211501","Schwaben","A#","Altenmünster","772115"],
                ["FF Baiershofen","7","72","115","2","14","14FW77211502","Schwaben","A#","Altenmünster","772115"],
                ["FF Eppishofen","7","72","115","3","14","14FW77211503","Schwaben","A#","Altenmünster","772115"],
                ["FF Hegnenbach","7","72","115","4","14","14FW77211504","Schwaben","A#","Altenmünster","772115"],
                ["FF Hennhofen","7","72","115","5","14","14FW77211505","Schwaben","A#","Altenmünster","772115"],
                ["FF Neumünster","7","72","115","6","14","14FW77211506","Schwaben","A#","Altenmünster","772115"],
                ["FF Unterschöneberg","7","72","115","7","14","14FW77211507","Schwaben","A#","Altenmünster","772115"],
                ["FF Zusamzell","7","72","115","8","14","14FW77211508","Schwaben","A#","Altenmünster","772115"],
                ["BF Augsburg I","7","61","","1","14","14FW76100001","Schwaben","A","Augsburg","761000"],
                ["BtF Flughafen Augsburg","7","61","","2","14","14FW76100002","Schwaben","A","Augsburg","761000"],
                ["BtF UPM-Kymmene Augsburg","7","61","","3","14","14FW76100003","Schwaben","A","Augsburg","761000"],
                ["FF Bergheim","7","61","","4","14","14FW76100004","Schwaben","A","Augsburg","761000"],
                ["FF Göggingen","7","61","","5","14","14FW76100005","Schwaben","A","Augsburg","761000"],
                ["FF Haunstetten","7","61","","6","14","14FW76100006","Schwaben","A","Augsburg","761000"],
                ["FF Inningen","7","61","","7","14","14FW76100007","Schwaben","A","Augsburg","761000"],
                ["FF Kriegshaber","7","61","","8","14","14FW76100008","Schwaben","A","Augsburg","761000"],
                ["FF Lechhausen","7","61","","9","14","14FW76100009","Schwaben","A","Augsburg","761000"],
                ["FF Oberhausen","7","61","","10","14","14FW76100010","Schwaben","A","Augsburg","761000"],
                ["FF Pfersee","7","61","","11","14","14FW76100011","Schwaben","A","Augsburg","761000"],
                ["WF Amann Nähgarne","7","61","","12","14","14FW76100012","Schwaben","A","Augsburg","761000"],
                ["WF MAN Augsburg","7","61","","13","14","14FW76100013","Schwaben","A","Augsburg","761000"],
                ["WF Premium Aerotech Augsburg","7","61","","14","14","14FW76100014","Schwaben","A","Augsburg","761000"],
                ["WF Von Roll","7","61","","15","14","14FW76100015","Schwaben","A","Augsburg","761000"],
                ["BF Augsburg II","7","61","","16","14","14FW76100016","Schwaben","A","Augsburg","761000"],
                ["BF Augsburg III","7","61","","17","14","14FW76100017","Schwaben","A","Augsburg","761000"],
                ["FF Aystetten","7","72","117","1","14","14FW77211701","Schwaben","A#","Aystetten","772117"],
                ["FF Affaltern","7","72","121","1","14","14FW77212101","Schwaben","A#","Biberbach","772121"],
                ["FF Biberbach","7","72","121","2","14","14FW77212102","Schwaben","A#","Biberbach","772121"],
                ["FF Eisenbrechtshofen","7","72","121","3","14","14FW77212103","Schwaben","A#","Biberbach","772121"],
                ["FF Feigenhofen","7","72","121","4","14","14FW77212104","Schwaben","A#","Biberbach","772121"],
                ["FF Markt","7","72","121","5","14","14FW77212105","Schwaben","A#","Biberbach","772121"],
                ["FF Bobingen","7","72","125","1","14","14FW77212501","Schwaben","A#","Bobingen","772125"],
                ["FF Reinhartshausen","7","72","125","2","14","14FW77212502","Schwaben","A#","Bobingen","772125"],
                ["FF Straßberg","7","72","125","3","14","14FW77212503","Schwaben","A#","Bobingen","772125"],
                ["FF Waldberg","7","72","125","4","14","14FW77212504","Schwaben","A#","Bobingen","772125"],
                ["WF IWB Bobingen","7","72","125","5","14","14FW77212505","Schwaben","A#","Bobingen","772125"],
                ["FF Bonstetten","7","72","126","1","14","14FW77212601","Schwaben","A#","Bonstetten","772126"],
                ["FF Anhausen","7","72","130","1","14","14FW77213001","Schwaben","A#","Diedorf","772130"],
                ["FF Biburg","7","72","130","2","14","14FW77213002","Schwaben","A#","Diedorf","772130"],
                ["FF Diedorf","7","72","130","3","14","14FW77213003","Schwaben","A#","Diedorf","772130"],
                ["FF Willishausen","7","72","130","4","14","14FW77213004","Schwaben","A#","Diedorf","772130"],
                ["FF Anried","7","72","131","1","14","14FW77213101","Schwaben","A#","Dinkelscherben","772131"],
                ["FF Breitenbronn","7","72","131","2","14","14FW77213102","Schwaben","A#","Dinkelscherben","772131"],
                ["FF Dinkelscherben","7","72","131","3","14","14FW77213103","Schwaben","A#","Dinkelscherben","772131"],
                ["FF Ettelried","7","72","131","4","14","14FW77213104","Schwaben","A#","Dinkelscherben","772131"],
                ["FF Fleinhausen","7","72","131","5","14","14FW77213105","Schwaben","A#","Dinkelscherben","772131"],
                ["FF Grünenbaindt","7","72","131","6","14","14FW77213106","Schwaben","A#","Dinkelscherben","772131"],
                ["FF Häder","7","72","131","7","14","14FW77213107","Schwaben","A#","Dinkelscherben","772131"],
                ["FF Lindach","7","72","131","8","14","14FW77213108","Schwaben","A#","Dinkelscherben","772131"],
                ["FF Oberschöneberg","7","72","131","9","14","14FW77213109","Schwaben","A#","Dinkelscherben","772131"],
                ["FF Ried","7","72","131","10","14","14FW77213110","Schwaben","A#","Dinkelscherben","772131"],
                ["FF Ehingen","7","72","134","1","14","14FW77213401","Schwaben","A#","Ehingen","772134"],
                ["FF Ortlfingen","7","72","134","2","14","14FW77213402","Schwaben","A#","Ehingen","772134"],
                ["FF Ellgau","7","72","136","1","14","14FW77213601","Schwaben","A#","Ellgau","772136"],
                ["FF Emersacker","7","72","137","1","14","14FW77213701","Schwaben","A#","Emersacker","772137"],
                ["FF Aretsried","7","72","141","1","14","14FW77214101","Schwaben","A#","Fischach","772141"],
                ["FF Fischach","7","72","141","2","14","14FW77214102","Schwaben","A#","Fischach","772141"],
                ["FF Reitenbuch","7","72","141","3","14","14FW77214103","Schwaben","A#","Fischach","772141"],
                ["FF Siegertshofen","7","72","141","4","14","14FW77214104","Schwaben","A#","Fischach","772141"],
                ["FF Tronetshofen","7","72","141","5","14","14FW77214105","Schwaben","A#","Fischach","772141"],
                ["FF Willmatshofen","7","72","141","6","14","14FW77214106","Schwaben","A#","Fischach","772141"],
                ["FF Wollmetshofen","7","72","141","7","14","14FW77214107","Schwaben","A#","Fischach","772141"],
                ["FF Gablingen","7","72","145","1","14","14FW77214501","Schwaben","A#","Gablingen","772145"],
                ["FF Lützelburg","7","72","145","2","14","14FW77214502","Schwaben","A#","Gablingen","772145"],
                ["FF Batzenhofen","7","72","147","1","14","14FW77214701","Schwaben","A#","Gersthofen","772147"],
                ["FF Edenbergen","7","72","147","2","14","14FW77214702","Schwaben","A#","Gersthofen","772147"],
                ["FF Gersthofen","7","72","147","3","14","14FW77214703","Schwaben","A#","Gersthofen","772147"],
                ["FF Hirblingen","7","72","147","4","14","14FW77214704","Schwaben","A#","Gersthofen","772147"],
                ["FF Rettenbergen","7","72","147","5","14","14FW77214705","Schwaben","A#","Gersthofen","772147"],
                ["WF IGS","7","72","147","6","14","14FW77214706","Schwaben","A#","Gersthofen","772147"],
                ["FF Deubach","7","72","148","1","14","14FW77214801","Schwaben","A#","Gessertshausen","772148"],
                ["FF Döpshofen","7","72","148","2","14","14FW77214802","Schwaben","A#","Gessertshausen","772148"],
                ["FF Gessertshausen","7","72","148","3","14","14FW77214803","Schwaben","A#","Gessertshausen","772148"],
                ["FF Margertshausen","7","72","148","4","14","14FW77214804","Schwaben","A#","Gessertshausen","772148"],
                ["FF Wollishausen","7","72","148","5","14","14FW77214805","Schwaben","A#","Gessertshausen","772148"],
                ["FF Graben","7","72","149","1","14","14FW77214901","Schwaben","A#","Graben","772149"],
                ["FF Großaitingen","7","72","151","1","14","14FW77215101","Schwaben","A#","Großaitingen","772151"],
                ["FF Reinhartshofen","7","72","151","2","14","14FW77215102","Schwaben","A#","Großaitingen","772151"],
                ["FF Heretsried","7","72","156","1","14","14FW77215601","Schwaben","A#","Heretsried","772156"],
                ["FF Lauterbrunn","7","72","156","2","14","14FW77215602","Schwaben","A#","Heretsried","772156"],
                ["FF Hiltenfingen","7","72","157","1","14","14FW77215701","Schwaben","A#","Hiltenfingen","772157"],
                ["FF Auerbach","7","72","159","1","14","14FW77215901","Schwaben","A#","Horgau","772159"],
                ["FF Horgau","7","72","159","2","14","14FW77215902","Schwaben","A#","Horgau","772159"],
                ["FF Horgauergreut","7","72","159","3","14","14FW77215903","Schwaben","A#","Horgau","772159"],
                ["FF Bieselbach","7","72","159","4","14","14FW77215904","Schwaben","A#","Horgau","772159"],
                ["FF Kleinaitingen","7","72","160","1","14","14FW77216001","Schwaben","A#","Kleinaitingen","772160"],
                ["FF Klosterlechfeld","7","72","162","1","14","14FW77216201","Schwaben","A#","Klosterlechfeld","772162"],
                ["FF Königsbrunn","7","72","163","1","14","14FW77216301","Schwaben","A#","Königsbrunn","772163"],
                ["FF Kühlenthal","7","72","166","1","14","14FW77216601","Schwaben","A#","Kühlenthal","772166"],
                ["FF Agawang","7","72","167","1","14","14FW77216701","Schwaben","A#","Kutzenhausen","772167"],
                ["FF Buch","7","72","167","2","14","14FW77216702","Schwaben","A#","Kutzenhausen","772167"],
                ["FF Kutzenhausen","7","72","167","3","14","14FW77216703","Schwaben","A#","Kutzenhausen","772167"],
                ["FF Maingründel","7","72","167","4","14","14FW77216704","Schwaben","A#","Kutzenhausen","772167"],
                ["FF Rommelsried","7","72","167","5","14","14FW77216705","Schwaben","A#","Kutzenhausen","772167"],
                ["FF Langenneufnach","7","72","168","1","14","14FW77216801","Schwaben","A#","Langenneufnach","772168"],
                ["FF Gennach","7","72","170","1","14","14FW77217001","Schwaben","A#","Langerringen","772170"],
                ["FF Langerringen","7","72","170","2","14","14FW77217002","Schwaben","A#","Langerringen","772170"],
                ["FF Schwabmühlhausen","7","72","170","3","14","14FW77217003","Schwaben","A#","Langerringen","772170"],
                ["FF Achsheim","7","72","171","1","14","14FW77217101","Schwaben","A#","Langweid a.Lech","772171"],
                ["FF Langweid","7","72","171","2","14","14FW77217102","Schwaben","A#","Langweid a.Lech","772171"],
                ["FF Stettenhofen","7","72","171","3","14","14FW77217103","Schwaben","A#","Langweid a.Lech","772171"],
                ["WF Archroma","7","72","171","4","14","14FW77217104","Schwaben","A#","Langweid a.Lech","772171"],
                ["FF Erlingen","7","72","177","1","14","14FW77217701","Schwaben","A#","Meitingen","772177"],
                ["FF Herbertshofen","7","72","177","2","14","14FW77217702","Schwaben","A#","Meitingen","772177"],
                ["FF Langenreichen","7","72","177","3","14","14FW77217703","Schwaben","A#","Meitingen","772177"],
                ["FF Meitingen","7","72","177","4","14","14FW77217704","Schwaben","A#","Meitingen","772177"],
                ["FF Ostendorf","7","72","177","5","14","14FW77217705","Schwaben","A#","Meitingen","772177"],
                ["FF Waltershofen","7","72","177","6","14","14FW77217706","Schwaben","A#","Meitingen","772177"],
                ["WF Lech-Stahlwerke","7","72","177","7","14","14FW77217707","Schwaben","A#","Meitingen","772177"],
                ["WF SGL Carbon","7","72","177","8","14","14FW77217708","Schwaben","A#","Meitingen","772177"],
                ["FF Grimoldsried","7","72","178","1","14","14FW77217801","Schwaben","A#","Mickhausen","772178"],
                ["FF Mickhausen","7","72","178","2","14","14FW77217802","Schwaben","A#","Mickhausen","772178"],
                ["FF Münster","7","72","178","3","14","14FW77217803","Schwaben","A#","Mickhausen","772178"],
                ["FF Mittelneufnach","7","72","179","1","14","14FW77217901","Schwaben","A#","Mittelneufnach","772179"],
                ["FF Reichertshofen","7","72","179","2","14","14FW77217902","Schwaben","A#","Mittelneufnach","772179"],
                ["FF Hainhofen","7","72","184","1","14","14FW77218401","Schwaben","A#","Neusäß","772184"],
                ["FF Hammel","7","72","184","2","14","14FW77218402","Schwaben","A#","Neusäß","772184"],
                ["FF Neusäß","7","72","184","3","14","14FW77218403","Schwaben","A#","Neusäß","772184"],
                ["FF Ottmarshausen","7","72","184","4","14","14FW77218404","Schwaben","A#","Neusäß","772184"],
                ["FF Schlipsheim","7","72","184","5","14","14FW77218405","Schwaben","A#","Neusäß","772184"],
                ["FF Steppach","7","72","184","6","14","14FW77218406","Schwaben","A#","Neusäß","772184"],
                ["FF Täfertingen","7","72","184","7","14","14FW77218407","Schwaben","A#","Neusäß","772184"],
                ["FF Westheim","7","72","184","8","14","14FW77218408","Schwaben","A#","Neusäß","772184"],
                ["FF Blankenburg","7","72","185","1","14","14FW77218501","Schwaben","A#","Nordendorf","772185"],
                ["FF Nordendorf","7","72","185","2","14","14FW77218502","Schwaben","A#","Nordendorf","772185"],
                ["FF Oberottmarshausen","7","72","186","1","14","14FW77218601","Schwaben","A#","Oberottmarshausen","772186"],
                ["FF Konradshofen","7","72","197","1","14","14FW77219701","Schwaben","A#","Scherstetten","772197"],
                ["FF Scherstetten","7","72","197","2","14","14FW77219702","Schwaben","A#","Scherstetten","772197"],
                ["FF Birkach","7","72","200","1","14","14FW77220001","Schwaben","A#","Schwabmünchen","772200"],
                ["FF Klimmach","7","72","200","2","14","14FW77220002","Schwaben","A#","Schwabmünchen","772200"],
                ["FF Mittelstetten","7","72","200","3","14","14FW77220003","Schwaben","A#","Schwabmünchen","772200"],
                ["FF Schwabegg","7","72","200","4","14","14FW77220004","Schwaben","A#","Schwabmünchen","772200"],
                ["FF Schwabmünchen","7","72","200","5","14","14FW77220005","Schwaben","A#","Schwabmünchen","772200"],
                ["WF Osram","7","72","200","6","14","14FW77220006","Schwaben","A#","Schwabmünchen","772200"],
                ["FF Deuringen","7","72","202","1","14","14FW77220201","Schwaben","A#","Stadtbergen","772202"],
                ["FF Leitershofen","7","72","202","2","14","14FW77220202","Schwaben","A#","Stadtbergen","772202"],
                ["FF Stadtbergen","7","72","202","3","14","14FW77220203","Schwaben","A#","Stadtbergen","772202"],
                ["FF Neukirchen","7","72","207","1","14","14FW77220701","Schwaben","A#","Thierhaupten","772207"],
                ["FF Thierhaupten","7","72","207","2","14","14FW77220702","Schwaben","A#","Thierhaupten","772207"],
                ["FF Untermeitingen","7","72","209","1","14","14FW77220901","Schwaben","A#","Untermeitingen","772209"],
                ["FF Ustersbach","7","72","211","1","14","14FW77221101","Schwaben","A#","Ustersbach","772211"],
                ["FF Walkertshofen","7","72","214","1","14","14FW77221401","Schwaben","A#","Walkertshofen","772214"],
                ["FF Wehringen","7","72","215","1","14","14FW77221501","Schwaben","A#","Wehringen","772215"],
                ["FF Reutern","7","72","216","1","14","14FW77221601","Schwaben","A#","Welden","772216"],
                ["FF Welden","7","72","216","2","14","14FW77221602","Schwaben","A#","Welden","772216"],
                ["FF Westendorf","7","72","217","1","14","14FW77221701","Schwaben","A#","Westendorf","772217"],
                ["FF Gabelbach","7","72","223","1","14","14FW77222301","Schwaben","A#","Zusmarshausen","772223"],
                ["FF Gabelbachergreut","7","72","223","2","14","14FW77222302","Schwaben","A#","Zusmarshausen","772223"],
                ["FF Steinekirch","7","72","223","3","14","14FW77222303","Schwaben","A#","Zusmarshausen","772223"],
                ["FF Streitheim","7","72","223","4","14","14FW77222304","Schwaben","A#","Zusmarshausen","772223"],
                ["FF Vallried","7","72","223","5","14","14FW77222305","Schwaben","A#","Zusmarshausen","772223"],
                ["FF Wollbach","7","72","223","6","14","14FW77222306","Schwaben","A#","Zusmarshausen","772223"],
                ["FF Wörleschwang","7","72","223","7","14","14FW77222307","Schwaben","A#","Zusmarshausen","772223"],
                ["FF Zusmarshausen","7","72","223","8","14","14FW77222308","Schwaben","A#","Zusmarshausen","772223"],
                ["FF Aislingen","7","73","111","1","14","14FW77311101","Schwaben","DLG","Aislingen","773111"],
                ["FF Baumgarten","7","73","111","2","14","14FW77311102","Schwaben","DLG","Aislingen","773111"],
                ["FF Bachhagel","7","73","112","1","14","14FW77311201","Schwaben","DLG","Bachhagel","773112"],
                ["FF Burghagel","7","73","112","2","14","14FW77311202","Schwaben","DLG","Bachhagel","773112"],
                ["FF Oberbechingen","7","73","112","3","14","14FW77311203","Schwaben","DLG","Bachhagel","773112"],
                ["FF Bächingen","7","73","113","1","14","14FW77311301","Schwaben","DLG","Bächingen a.d.Brenz","773113"],
                ["FF Binswangen","7","73","116","1","14","14FW77311601","Schwaben","DLG","Binswangen","773116"],
                ["FF Bissingen","7","73","117","1","14","14FW77311701","Schwaben","DLG","Bissingen","773117"],
                ["FF Diemantstein","7","73","117","2","14","14FW77311702","Schwaben","DLG","Bissingen","773117"],
                ["FF Fronhofen","7","73","117","3","14","14FW77311703","Schwaben","DLG","Bissingen","773117"],
                ["FF Göllingen","7","73","117","4","14","14FW77311704","Schwaben","DLG","Bissingen","773117"],
                ["FF Hochstein","7","73","117","5","14","14FW77311705","Schwaben","DLG","Bissingen","773117"],
                ["FF Kesselostheim","7","73","117","6","14","14FW77311706","Schwaben","DLG","Bissingen","773117"],
                ["FF Leiheim","7","73","117","7","14","14FW77311707","Schwaben","DLG","Bissingen","773117"],
                ["FF Oberliezheim","7","73","117","8","14","14FW77311708","Schwaben","DLG","Bissingen","773117"],
                ["FF Oberringingen","7","73","117","9","14","14FW77311709","Schwaben","DLG","Bissingen","773117"],
                ["FF Stillnau","7","73","117","10","14","14FW77311710","Schwaben","DLG","Bissingen","773117"],
                ["FF Thalheim","7","73","117","11","14","14FW77311711","Schwaben","DLG","Bissingen","773117"],
                ["FF Unterbissingen","7","73","117","12","14","14FW77311712","Schwaben","DLG","Bissingen","773117"],
                ["FF Unterringingen","7","73","117","13","14","14FW77311713","Schwaben","DLG","Bissingen","773117"],
                ["FF Zoltingen","7","73","117","14","14","14FW77311714","Schwaben","DLG","Bissingen","773117"],
                ["FF Blindheim","7","73","119","1","14","14FW77311901","Schwaben","DLG","Blindheim","773119"],
                ["FF Unterglauheim","7","73","119","2","14","14FW77311902","Schwaben","DLG","Blindheim","773119"],
                ["FF Wolpertstetten","7","73","119","3","14","14FW77311903","Schwaben","DLG","Blindheim","773119"],
                ["FF Buttenwiesen","7","73","122","1","14","14FW77312201","Schwaben","DLG","Buttenwiesen","773122"],
                ["FF Frauenstetten","7","73","122","2","14","14FW77312202","Schwaben","DLG","Buttenwiesen","773122"],
                ["FF Lauterbach","7","73","122","3","14","14FW77312203","Schwaben","DLG","Buttenwiesen","773122"],
                ["FF Pfaffenhofen","7","73","122","4","14","14FW77312204","Schwaben","DLG","Buttenwiesen","773122"],
                ["FF Thürheim","7","73","122","5","14","14FW77312205","Schwaben","DLG","Buttenwiesen","773122"],
                ["FF Wortelstetten","7","73","122","6","14","14FW77312206","Schwaben","DLG","Buttenwiesen","773122"],
                ["FF Dillingen","7","73","125","1","14","14FW77312501","Schwaben","DLG","Dillingen a.d.Donau","773125"],
                ["FF Donaualtheim","7","73","125","2","14","14FW77312502","Schwaben","DLG","Dillingen a.d.Donau","773125"],
                ["FF Fristingen","7","73","125","3","14","14FW77312503","Schwaben","DLG","Dillingen a.d.Donau","773125"],
                ["FF Hausen","7","73","125","4","14","14FW77312504","Schwaben","DLG","Dillingen a.d.Donau","773125"],
                ["FF Kicklingen","7","73","125","5","14","14FW77312505","Schwaben","DLG","Dillingen a.d.Donau","773125"],
                ["FF Schretzheim","7","73","125","6","14","14FW77312506","Schwaben","DLG","Dillingen a.d.Donau","773125"],
                ["FF Steinheim","7","73","125","7","14","14FW77312507","Schwaben","DLG","Dillingen a.d.Donau","773125"],
                ["WF Bosch-Siemens","7","73","125","8","14","14FW77312508","Schwaben","DLG","Dillingen a.d.Donau","773125"],
                ["WF Fahr","7","73","125","9","14","14FW77312509","Schwaben","DLG","Dillingen a.d.Donau","773125"],
                ["FF Finningen","7","73","150","1","14","14FW77315001","Schwaben","DLG","Finningen","773150"],
                ["FF Mörslingen","7","73","150","2","14","14FW77315002","Schwaben","DLG","Finningen","773150"],
                ["FF Glött","7","73","133","1","14","14FW77313301","Schwaben","DLG","Glött","773133"],
                ["FF Echenbrunn","7","73","136","1","14","14FW77313601","Schwaben","DLG","Gundelfingen a.d.Donau","773136"],
                ["FF Gundelfingen","7","73","136","2","14","14FW77313602","Schwaben","DLG","Gundelfingen a.d.Donau","773136"],
                ["FF Peterswörth","7","73","136","3","14","14FW77313603","Schwaben","DLG","Gundelfingen a.d.Donau","773136"],
                ["WF Gartner GmbH","7","73","136","4","14","14FW77313604","Schwaben","DLG","Gundelfingen a.d.Donau","773136"],
                ["FF Haunsheim","7","73","137","1","14","14FW77313701","Schwaben","DLG","Haunsheim","773137"],
                ["FF Unterbechingen","7","73","137","2","14","14FW77313702","Schwaben","DLG","Haunsheim","773137"],
                ["FF Deisenhofen","7","73","139","1","14","14FW77313901","Schwaben","DLG","Höchstädt a.d.Donau","773139"],
                ["FF Höchstädt","7","73","139","2","14","14FW77313902","Schwaben","DLG","Höchstädt a.d.Donau","773139"],
                ["FF Oberglauheim","7","73","139","3","14","14FW77313903","Schwaben","DLG","Höchstädt a.d.Donau","773139"],
                ["FF Schwennenbach","7","73","139","4","14","14FW77313904","Schwaben","DLG","Höchstädt a.d.Donau","773139"],
                ["FF Sonderheim","7","73","139","5","14","14FW77313905","Schwaben","DLG","Höchstädt a.d.Donau","773139"],
                ["FF Altenbaindt","7","73","140","1","14","14FW77314001","Schwaben","DLG","Holzheim","773140"],
                ["FF Ellerbach","7","73","140","2","14","14FW77314002","Schwaben","DLG","Holzheim","773140"],
                ["FF Eppisburg","7","73","140","3","14","14FW77314003","Schwaben","DLG","Holzheim","773140"],
                ["FF Holzheim","7","73","140","4","14","14FW77314004","Schwaben","DLG","Holzheim","773140"],
                ["FF Weisingen","7","73","140","5","14","14FW77314005","Schwaben","DLG","Holzheim","773140"],
                ["FF Asbach","7","73","143","1","14","14FW77314301","Schwaben","DLG","Laugna","773143"],
                ["FF Bocksberg","7","73","143","2","14","14FW77314302","Schwaben","DLG","Laugna","773143"],
                ["FF Laugna","7","73","143","3","14","14FW77314303","Schwaben","DLG","Laugna","773143"],
                ["FF Osterbuch","7","73","143","4","14","14FW77314304","Schwaben","DLG","Laugna","773143"],
                ["FF Frauenriedhausen","7","73","144","1","14","14FW77314401","Schwaben","DLG","Lauingen (Donau)","773144"],
                ["FF Lauingen","7","73","144","2","14","14FW77314402","Schwaben","DLG","Lauingen (Donau)","773144"],
                ["FF Veitriedhausen","7","73","144","3","14","14FW77314403","Schwaben","DLG","Lauingen (Donau)","773144"],
                ["FF Lutzingen","7","73","146","1","14","14FW77314601","Schwaben","DLG","Lutzingen","773146"],
                ["FF Unterliezheim","7","73","146","2","14","14FW77314602","Schwaben","DLG","Lutzingen","773146"],
                ["FF Obermedlingen","7","73","153","1","14","14FW77315301","Schwaben","DLG","Medlingen","773153"],
                ["FF Untermedlingen","7","73","153","2","14","14FW77315302","Schwaben","DLG","Medlingen","773153"],
                ["FF Bergheim","7","73","147","1","14","14FW77314701","Schwaben","DLG","Mödingen","773147"],
                ["FF Mödingen","7","73","147","2","14","14FW77314702","Schwaben","DLG","Mödingen","773147"],
                ["FF Gremheim","7","73","164","1","14","14FW77316401","Schwaben","DLG","Schwenningen","773164"],
                ["FF Schwenningen","7","73","164","2","14","14FW77316402","Schwaben","DLG","Schwenningen","773164"],
                ["FF Landshausen","7","73","170","1","14","14FW77317001","Schwaben","DLG","Syrgenstein","773170"],
                ["FF Staufen","7","73","170","2","14","14FW77317002","Schwaben","DLG","Syrgenstein","773170"],
                ["FF Syrgenstein","7","73","170","3","14","14FW77317003","Schwaben","DLG","Syrgenstein","773170"],
                ["FF Riedsend","7","73","179","1","14","14FW77317901","Schwaben","DLG","Villenbach","773179"],
                ["FF Villenbach","7","73","179","2","14","14FW77317902","Schwaben","DLG","Villenbach","773179"],
                ["FF Wengen","7","73","179","3","14","14FW77317903","Schwaben","DLG","Villenbach","773179"],
                ["FF Bliensbach","7","73","182","1","14","14FW77318201","Schwaben","DLG","Wertingen","773182"],
                ["FF Gottmannshofen","7","73","182","2","14","14FW77318202","Schwaben","DLG","Wertingen","773182"],
                ["FF Hirschbach","7","73","182","3","14","14FW77318203","Schwaben","DLG","Wertingen","773182"],
                ["FF Hohenreichen","7","73","182","4","14","14FW77318204","Schwaben","DLG","Wertingen","773182"],
                ["FF Prettelshofen","7","73","182","5","14","14FW77318205","Schwaben","DLG","Wertingen","773182"],
                ["FF Rieblingen","7","73","182","6","14","14FW77318206","Schwaben","DLG","Wertingen","773182"],
                ["FF Roggden","7","73","182","7","14","14FW77318207","Schwaben","DLG","Wertingen","773182"],
                ["FF Wertingen","7","73","182","8","14","14FW77318208","Schwaben","DLG","Wertingen","773182"],
                ["FF Schabringen","7","73","183","1","14","14FW77318301","Schwaben","DLG","Wittislingen","773183"],
                ["FF Wittislingen","7","73","183","2","14","14FW77318302","Schwaben","DLG","Wittislingen","773183"],
                ["FF Reistingen","7","73","186","1","14","14FW77318601","Schwaben","DLG","Ziertheim","773186"],
                ["FF Ziertheim","7","73","186","2","14","14FW77318602","Schwaben","DLG","Ziertheim","773186"],
                ["FF Zöschingen","7","73","187","1","14","14FW77318701","Schwaben","DLG","Zöschingen","773187"],
                ["FF Sontheim","7","73","188","1","14","14FW77318801","Schwaben","DLG","Zusamaltheim","773188"],
                ["FF Zusamaltheim","7","73","188","2","14","14FW77318802","Schwaben","DLG","Zusamaltheim","773188"],
                ["FF Alerheim","7","79","111","1","14","14FW77911101","Schwaben","DON","Alerheim","779111"],
                ["FF Bühl","7","79","111","2","14","14FW77911102","Schwaben","DON","Alerheim","779111"],
                ["FF Rudelstetten","7","79","111","3","14","14FW77911103","Schwaben","DON","Alerheim","779111"],
                ["FF Wörnitzostheim","7","79","111","4","14","14FW77911104","Schwaben","DON","Alerheim","779111"],
                ["FF Amerdingen","7","79","112","1","14","14FW77911201","Schwaben","DON","Amerdingen","779112"],
                ["FF Bollstadt","7","79","112","2","14","14FW77911202","Schwaben","DON","Amerdingen","779112"],
                ["FF Asbach-Bäumenheim","7","79","115","1","14","14FW77911501","Schwaben","DON","Asbach-Bäumenheim","779115"],
                ["FF Hamlar","7","79","115","2","14","14FW77911502","Schwaben","DON","Asbach-Bäumenheim","779115"],
                ["WF FENDT Asbach-Bäumenheim","7","79","115","3","14","14FW77911503","Schwaben","DON","Asbach-Bäumenheim","779115"],
                ["FF Auhausen","7","79","117","1","14","14FW77911701","Schwaben","DON","Auhausen","779117"],
                ["FF Dornstadt","7","79","117","2","14","14FW77911702","Schwaben","DON","Auhausen","779117"],
                ["FF Lochenbach","7","79","117","3","14","14FW77911703","Schwaben","DON","Auhausen","779117"],
                ["FF Baierfeld","7","79","126","1","14","14FW77912601","Schwaben","DON","Buchdorf","779126"],
                ["FF Buchdorf","7","79","126","2","14","14FW77912602","Schwaben","DON","Buchdorf","779126"],
                ["FF Daiting","7","79","129","1","14","14FW77912901","Schwaben","DON","Daiting","779129"],
                ["FF Hochfeld","7","79","129","2","14","14FW77912902","Schwaben","DON","Daiting","779129"],
                ["FF Natterholz","7","79","129","3","14","14FW77912903","Schwaben","DON","Daiting","779129"],
                ["FF Deiningen","7","79","130","1","14","14FW77913001","Schwaben","DON","Deiningen","779130"],
                ["FF Auchsesheim","7","79","131","1","14","14FW77913101","Schwaben","DON","Donauwörth","779131"],
                ["FF Berg","7","79","131","2","14","14FW77913102","Schwaben","DON","Donauwörth","779131"],
                ["FF Donauwörth","7","79","131","3","14","14FW77913103","Schwaben","DON","Donauwörth","779131"],
                ["FF Nordheim","7","79","131","4","14","14FW77913104","Schwaben","DON","Donauwörth","779131"],
                ["FF Riedlingen","7","79","131","5","14","14FW77913105","Schwaben","DON","Donauwörth","779131"],
                ["FF Schäfstall","7","79","131","6","14","14FW77913106","Schwaben","DON","Donauwörth","779131"],
                ["FF Wörnitzstein","7","79","131","7","14","14FW77913107","Schwaben","DON","Donauwörth","779131"],
                ["FF Zirgesheim","7","79","131","8","14","14FW77913108","Schwaben","DON","Donauwörth","779131"],
                ["WF Airbus","7","79","131","9","14","14FW77913109","Schwaben","DON","Donauwörth","779131"],
                ["FF Ederheim","7","79","136","1","14","14FW77913601","Schwaben","DON","Ederheim","779136"],
                ["FF Hürnheim","7","79","136","2","14","14FW77913602","Schwaben","DON","Ederheim","779136"],
                ["FF Belzheim","7","79","138","1","14","14FW77913801","Schwaben","DON","Ehingen a.Ries","779138"],
                ["FF Ehingen","7","79","138","2","14","14FW77913802","Schwaben","DON","Ehingen a.Ries","779138"],
                ["FF Aufhausen","7","79","146","1","14","14FW77914601","Schwaben","DON","Forheim","779146"],
                ["FF Forheim","7","79","146","2","14","14FW77914602","Schwaben","DON","Forheim","779146"],
                ["FF Fremdingen","7","79","147","1","14","14FW77914701","Schwaben","DON","Fremdingen","779147"],
                ["FF Hausen","7","79","147","2","14","14FW77914702","Schwaben","DON","Fremdingen","779147"],
                ["FF Herblingen","7","79","147","3","14","14FW77914703","Schwaben","DON","Fremdingen","779147"],
                ["FF Hochaltingen","7","79","147","4","14","14FW77914704","Schwaben","DON","Fremdingen","779147"],
                ["FF Schopflohe","7","79","147","5","14","14FW77914705","Schwaben","DON","Fremdingen","779147"],
                ["FF Seglohe","7","79","147","6","14","14FW77914706","Schwaben","DON","Fremdingen","779147"],
                ["FF Fünfstetten","7","79","148","1","14","14FW77914801","Schwaben","DON","Fünfstetten","779148"],
                ["FF Nußbühl-Heidmersbrunn","7","79","148","2","14","14FW77914802","Schwaben","DON","Fünfstetten","779148"],
                ["FF Genderkingen","7","79","149","1","14","14FW77914901","Schwaben","DON","Genderkingen","779149"],
                ["FF Hainsfarth","7","79","154","1","14","14FW77915401","Schwaben","DON","Hainsfarth","779154"],
                ["FF Steinhart","7","79","154","2","14","14FW77915402","Schwaben","DON","Hainsfarth","779154"],
                ["FF Brünsee-Marbach","7","79","155","1","14","14FW77915501","Schwaben","DON","Harburg (Schwaben)","779155"],
                ["FF Ebermergen","7","79","155","2","14","14FW77915502","Schwaben","DON","Harburg (Schwaben)","779155"],
                ["FF Großsorheim","7","79","155","3","14","14FW77915503","Schwaben","DON","Harburg (Schwaben)","779155"],
                ["FF Harburg","7","79","155","4","14","14FW77915504","Schwaben","DON","Harburg (Schwaben)","779155"],
                ["FF Heroldingen","7","79","155","5","14","14FW77915505","Schwaben","DON","Harburg (Schwaben)","779155"],
                ["FF Hoppingen","7","79","155","6","14","14FW77915506","Schwaben","DON","Harburg (Schwaben)","779155"],
                ["FF Mauren","7","79","155","7","14","14FW77915507","Schwaben","DON","Harburg (Schwaben)","779155"],
                ["FF Mündling","7","79","155","8","14","14FW77915508","Schwaben","DON","Harburg (Schwaben)","779155"],
                ["FF Ronheim","7","79","155","9","14","14FW77915509","Schwaben","DON","Harburg (Schwaben)","779155"],
                ["FF Schrattenhofen","7","79","155","10","14","14FW77915510","Schwaben","DON","Harburg (Schwaben)","779155"],
                ["FF Hohenaltheim","7","79","162","1","14","14FW77916201","Schwaben","DON","Hohenaltheim","779162"],
                ["FF Niederaltheim","7","79","162","2","14","14FW77916202","Schwaben","DON","Hohenaltheim","779162"],
                ["FF Bergendorf","7","79","163","1","14","14FW77916301","Schwaben","DON","Holzheim","779163"],
                ["FF Holzheim","7","79","163","2","14","14FW77916302","Schwaben","DON","Holzheim","779163"],
                ["FF Pessenburgheim","7","79","163","3","14","14FW77916303","Schwaben","DON","Holzheim","779163"],
                ["FF Riedheim-Stadel","7","79","163","4","14","14FW77916304","Schwaben","DON","Holzheim","779163"],
                ["FF Gosheim","7","79","167","1","14","14FW77916701","Schwaben","DON","Huisheim","779167"],
                ["FF Huisheim","7","79","167","2","14","14FW77916702","Schwaben","DON","Huisheim","779167"],
                ["FF Altisheim","7","79","169","1","14","14FW77916901","Schwaben","DON","Kaisheim","779169"],
                ["FF Bergstetten","7","79","169","2","14","14FW77916902","Schwaben","DON","Kaisheim","779169"],
                ["FF Gunzenheim","7","79","169","3","14","14FW77916903","Schwaben","DON","Kaisheim","779169"],
                ["FF Hafenreuth","7","79","169","4","14","14FW77916904","Schwaben","DON","Kaisheim","779169"],
                ["FF Kaisheim","7","79","169","5","14","14FW77916905","Schwaben","DON","Kaisheim","779169"],
                ["FF Leitheim","7","79","169","6","14","14FW77916906","Schwaben","DON","Kaisheim","779169"],
                ["FF Sulzdorf","7","79","169","7","14","14FW77916907","Schwaben","DON","Kaisheim","779169"],
                ["WF JVA Kaisheim","7","79","169","8","14","14FW77916908","Schwaben","DON","Kaisheim","779169"],
                ["FF Maihingen","7","79","176","1","14","14FW77917601","Schwaben","DON","Maihingen","779176"],
                ["FF Utzwingen","7","79","176","2","14","14FW77917602","Schwaben","DON","Maihingen","779176"],
                ["FF Marktoffingen","7","79","177","1","14","14FW77917701","Schwaben","DON","Marktoffingen","779177"],
                ["FF Minderoffingen","7","79","177","2","14","14FW77917702","Schwaben","DON","Marktoffingen","779177"],
                ["FF Burgmannshofen","7","79","178","1","14","14FW77917801","Schwaben","DON","Marxheim","779178"],
                ["FF Gansheim","7","79","178","2","14","14FW77917802","Schwaben","DON","Marxheim","779178"],
                ["FF Graisbach","7","79","178","3","14","14FW77917803","Schwaben","DON","Marxheim","779178"],
                ["FF Lechsend","7","79","178","4","14","14FW77917804","Schwaben","DON","Marxheim","779178"],
                ["FF Marxheim","7","79","178","5","14","14FW77917805","Schwaben","DON","Marxheim","779178"],
                ["FF Neuhausen","7","79","178","6","14","14FW77917806","Schwaben","DON","Marxheim","779178"],
                ["FF Schweinspoint","7","79","178","7","14","14FW77917807","Schwaben","DON","Marxheim","779178"],
                ["FF Megesheim","7","79","180","1","14","14FW77918001","Schwaben","DON","Megesheim","779180"],
                ["FF Druisheim","7","79","181","1","14","14FW77918101","Schwaben","DON","Mertingen","779181"],
                ["FF Heißesheim","7","79","181","2","14","14FW77918102","Schwaben","DON","Mertingen","779181"],
                ["FF Mertingen","7","79","181","3","14","14FW77918103","Schwaben","DON","Mertingen","779181"],
                ["FF Merzingen","7","79","184","1","14","14FW77918401","Schwaben","DON","Mönchsdeggingen","779184"],
                ["FF Mönchsdeggingen","7","79","184","2","14","14FW77918402","Schwaben","DON","Mönchsdeggingen","779184"],
                ["FF Rohrbach","7","79","184","3","14","14FW77918403","Schwaben","DON","Mönchsdeggingen","779184"],
                ["FF Schaffhausen","7","79","184","4","14","14FW77918404","Schwaben","DON","Mönchsdeggingen","779184"],
                ["FF Untermagerbein","7","79","184","5","14","14FW77918405","Schwaben","DON","Mönchsdeggingen","779184"],
                ["FF Ziswingen","7","79","184","6","14","14FW77918406","Schwaben","DON","Mönchsdeggingen","779184"],
                ["FF Flotzheim","7","79","186","1","14","14FW77918601","Schwaben","DON","Monheim","779186"],
                ["FF Itzing","7","79","186","2","14","14FW77918602","Schwaben","DON","Monheim","779186"],
                ["FF Kölburg","7","79","186","3","14","14FW77918603","Schwaben","DON","Monheim","779186"],
                ["FF Monheim","7","79","186","4","14","14FW77918604","Schwaben","DON","Monheim","779186"],
                ["FF Rehau","7","79","186","5","14","14FW77918605","Schwaben","DON","Monheim","779186"],
                ["FF Ried","7","79","186","6","14","14FW77918606","Schwaben","DON","Monheim","779186"],
                ["FF Warching","7","79","186","7","14","14FW77918607","Schwaben","DON","Monheim","779186"],
                ["FF Weilheim","7","79","186","8","14","14FW77918608","Schwaben","DON","Monheim","779186"],
                ["FF Wittesheim","7","79","186","9","14","14FW77918609","Schwaben","DON","Monheim","779186"],
                ["FF Appetshofen-Lierheim","7","79","185","1","14","14FW77918501","Schwaben","DON","Möttingen","779185"],
                ["FF Balgheim","7","79","185","2","14","14FW77918502","Schwaben","DON","Möttingen","779185"],
                ["FF Enkingen","7","79","185","3","14","14FW77918503","Schwaben","DON","Möttingen","779185"],
                ["FF Kleinsorheim","7","79","185","4","14","14FW77918504","Schwaben","DON","Möttingen","779185"],
                ["FF Möttingen","7","79","185","5","14","14FW77918505","Schwaben","DON","Möttingen","779185"],
                ["FF Laub","7","79","188","1","14","14FW77918801","Schwaben","DON","Munningen","779188"],
                ["FF Munningen","7","79","188","2","14","14FW77918802","Schwaben","DON","Munningen","779188"],
                ["FF Schwörsheim","7","79","188","3","14","14FW77918803","Schwaben","DON","Munningen","779188"],
                ["FF Münster","7","79","187","1","14","14FW77918701","Schwaben","DON","Münster","779187"],
                ["FF Feldheim","7","79","192","1","14","14FW77919201","Schwaben","DON","Niederschönenfeld","779192"],
                ["FF Niederschönenfeld","7","79","192","2","14","14FW77919202","Schwaben","DON","Niederschönenfeld","779192"],
                ["WF JVA Niederschönenfeld","7","79","192","3","14","14FW77919203","Schwaben","DON","Niederschönenfeld","779192"],
                ["FF Baldingen","7","79","194","1","14","14FW77919401","Schwaben","DON","Nördlingen","779194"],
                ["FF Dürrenzimmern","7","79","194","2","14","14FW77919402","Schwaben","DON","Nördlingen","779194"],
                ["FF Grosselfingen","7","79","194","3","14","14FW77919403","Schwaben","DON","Nördlingen","779194"],
                ["FF Herkheim","7","79","194","4","14","14FW77919404","Schwaben","DON","Nördlingen","779194"],
                ["FF Holheim","7","79","194","5","14","14FW77919405","Schwaben","DON","Nördlingen","779194"],
                ["FF Kleinerdlingen","7","79","194","6","14","14FW77919406","Schwaben","DON","Nördlingen","779194"],
                ["FF Löpsingen","7","79","194","7","14","14FW77919407","Schwaben","DON","Nördlingen","779194"],
                ["FF Nähermemmingen","7","79","194","8","14","14FW77919408","Schwaben","DON","Nördlingen","779194"],
                ["FF Nördlingen","7","79","194","9","14","14FW77919409","Schwaben","DON","Nördlingen","779194"],
                ["FF Pfäfflingen","7","79","194","10","14","14FW77919410","Schwaben","DON","Nördlingen","779194"],
                ["FF Schmähingen","7","79","194","11","14","14FW77919411","Schwaben","DON","Nördlingen","779194"],
                ["WF DS Smith Packaging","7","79","194","12","14","14FW77919412","Schwaben","DON","Nördlingen","779194"],
                ["FF Eggelstetten","7","79","196","1","14","14FW77919601","Schwaben","DON","Oberndorf a.Lech","779196"],
                ["FF Oberndorf","7","79","196","2","14","14FW77919602","Schwaben","DON","Oberndorf a.Lech","779196"],
                ["BtF JELD-WEN Oettingen","7","79","197","1","14","14FW77919701","Schwaben","DON","Oettingen i.Bay.","779197"],
                ["FF Erlbach","7","79","197","2","14","14FW77919702","Schwaben","DON","Oettingen i.Bay.","779197"],
                ["FF Heuberg","7","79","197","3","14","14FW77919703","Schwaben","DON","Oettingen i.Bay.","779197"],
                ["FF Lehmingen","7","79","197","4","14","14FW77919704","Schwaben","DON","Oettingen i.Bay.","779197"],
                ["FF Niederhofen","7","79","197","5","14","14FW77919705","Schwaben","DON","Oettingen i.Bay.","779197"],
                ["FF Nittingen","7","79","197","6","14","14FW77919706","Schwaben","DON","Oettingen i.Bay.","779197"],
                ["FF Oettingen","7","79","197","7","14","14FW77919707","Schwaben","DON","Oettingen i.Bay.","779197"],
                ["FF Otting","7","79","198","1","14","14FW77919801","Schwaben","DON","Otting","779198"],
                ["BtF SÜDZUCKER Rain","7","79","201","1","14","14FW77920101","Schwaben","DON","Rain","779201"],
                ["FF Bayerdilling","7","79","201","2","14","14FW77920102","Schwaben","DON","Rain","779201"],
                ["FF Etting","7","79","201","3","14","14FW77920103","Schwaben","DON","Rain","779201"],
                ["FF Gempfing","7","79","201","4","14","14FW77920104","Schwaben","DON","Rain","779201"],
                ["FF Mittelstetten","7","79","201","5","14","14FW77920105","Schwaben","DON","Rain","779201"],
                ["FF Oberpeiching","7","79","201","6","14","14FW77920106","Schwaben","DON","Rain","779201"],
                ["FF Rain","7","79","201","7","14","14FW77920107","Schwaben","DON","Rain","779201"],
                ["FF Sallach","7","79","201","8","14","14FW77920108","Schwaben","DON","Rain","779201"],
                ["FF Staudheim","7","79","201","9","14","14FW77920109","Schwaben","DON","Rain","779201"],
                ["FF Unterpeiching","7","79","201","10","14","14FW77920110","Schwaben","DON","Rain","779201"],
                ["FF Wächtering","7","79","201","11","14","14FW77920111","Schwaben","DON","Rain","779201"],
                ["FF Wallerdorf","7","79","201","12","14","14FW77920112","Schwaben","DON","Rain","779201"],
                ["FF Reimlingen","7","79","203","1","14","14FW77920301","Schwaben","DON","Reimlingen","779203"],
                ["FF Rögling","7","79","206","1","14","14FW77920601","Schwaben","DON","Rögling","779206"],
                ["FF Blossenau","7","79","217","1","14","14FW77921701","Schwaben","DON","Tagmersheim","779217"],
                ["FF Tagmersheim","7","79","217","2","14","14FW77921702","Schwaben","DON","Tagmersheim","779217"],
                ["FF Brachstadt","7","79","218","1","14","14FW77921801","Schwaben","DON","Tapfheim","779218"],
                ["FF Donaumünster-Erlingshofen","7","79","218","2","14","14FW77921802","Schwaben","DON","Tapfheim","779218"],
                ["FF Oppertshofen","7","79","218","3","14","14FW77921803","Schwaben","DON","Tapfheim","779218"],
                ["FF Tapfheim","7","79","218","4","14","14FW77921804","Schwaben","DON","Tapfheim","779218"],
                ["FF Zusum-Rettingen","7","79","218","5","14","14FW77921805","Schwaben","DON","Tapfheim","779218"],
                ["FF Birkhausen","7","79","224","1","14","14FW77922401","Schwaben","DON","Wallerstein","779224"],
                ["FF Ehringen","7","79","224","2","14","14FW77922402","Schwaben","DON","Wallerstein","779224"],
                ["FF Munzingen","7","79","224","3","14","14FW77922403","Schwaben","DON","Wallerstein","779224"],
                ["FF Wallerstein","7","79","224","4","14","14FW77922404","Schwaben","DON","Wallerstein","779224"],
                ["FF Fessenheim","7","79","226","1","14","14FW77922601","Schwaben","DON","Wechingen","779226"],
                ["FF Holzkirchen","7","79","226","2","14","14FW77922602","Schwaben","DON","Wechingen","779226"],
                ["FF Wechingen","7","79","226","3","14","14FW77922603","Schwaben","DON","Wechingen","779226"],
                ["BtF VALEO Autoelectric Wemding","7","79","228","1","14","14FW77922801","Schwaben","DON","Wemding","779228"],
                ["FF Amerbach","7","79","228","2","14","14FW77922802","Schwaben","DON","Wemding","779228"],
                ["FF Wemding","7","79","228","3","14","14FW77922803","Schwaben","DON","Wemding","779228"],
                ["FF Hagau","7","79","231","1","14","14FW77923101","Schwaben","DON","Wolferstadt","779231"],
                ["FF Wolferstadt","7","79","231","2","14","14FW77923102","Schwaben","DON","Wolferstadt","779231"],
                ["FF Zwerchstraß","7","79","231","3","14","14FW77923103","Schwaben","DON","Wolferstadt","779231"]
                ]

    
    def __init__(self, rows, filename: str = "dfm_import.xlsx"):
        
        self.rows = rows
        download_dir = Path.home() / "Downloads"

        download_dir.mkdir(parents=True, exist_ok=True)

        self.output_path = download_dir / filename

        self.wb = Workbook()
        self.ws = self.wb.active
        self.ws.title = "DFM Import"

    """
    def build(self):
    
            export_rows = []
    
            for row in self.rows:
    
                export_rows.append(
                    self._build_row(row)
                )
    
            return self.HEADERS, export_rows
    """
        
    def _build_row(self, row):

            eg_typ = Device.objects.get(tei = row["tei"])
            print(f'tei:{row["tei"]}, hersteller:{row["hersteller"]}, {eg_typ}')
            return [
    
                    row["tei"],
    
                    row["hersteller"],
    
                    eg_typ,
    
                    row["eg_art"],
    
                    self._betriebsstelle,
    
                    row["seriennummer"],
    
                    "",
    
                    "",
    
                    "",
    
                    "",
    
                    "kA",
    
                    "",
    
                    "",
    
                    "",
    
                    "",
                    
                    "",
                        
                    "",
                        
                    "",
                        
                    "",
                        
                    "",
                        
                    "",
                        
                    "",
                        
                    "",
                        
                    "",
                        
                    "",
                        
                    "",
                        
                    row["issi"],
                    
                    "kA",
                    
                    "",
                    
                    self._opta,
    
                    ]
            
    def _betriebsstelle(self, row):
        
        betriebsstelle = ""
        print("jetzt bin ich hier!")
        
        for i in self.datalist:
            if row["kommune"] == i[9] and row["landkreis"] == i[8]:
                print("hier bin ich!")
                betriebsstelle = i[6]
            else:
                pass
            
        return betriebsstelle
        
    def _opta(self, row):
        
        import re
        
        opta = 'BYFW_' + row["aopta_t"] + row["aopta_u"] + row["aopta_v"] + row["aopta_w"] + row["aopta_x"] + row["aopta_y"] + row["aopta_z"] + row["aopta_aa"] + row["aopta_ab"] + row["aopta_ac"] + row["aopta_ad"] + row["aopta_ae"] + row["aopta_af"] + row["aopta_ag"] + row["aopta_ah"] + row["aopta_ai"]
        prefix = opta[:-4]
        variable = opta[-4:]

        # Fall: DT11 -> DT 1 1
        if re.match(r"^[A-Za-z]{2}\d{2}$", variable):
            return f"{prefix}{variable[:2]} {variable[2]} {variable[3]}"

        # Fall: 1111 -> 11 11
        # Fall: 4021 -> 40 21
        return f"{prefix} {variable[:2]} {variable[2:]}"

    """
    def export(self):

        self.ws.append(self.HEADERS)

        for row in self.build:
            self.ws.append(row)

        self.wb.save(self.output_path)
        print(f"Datei erfolgreich gespeichert unter: {self.output_path.resolve()}")
    """
        
    def build(self):

        self.ws.append(self.HEADERS)
        written_rows = []
        
        for row in self.rows:

            device_obj = Device.objects.get(tei=row["tei"])
            eg_typ = str(device_obj.geraetename)
            betriebsstelle = str(self._betriebsstelle(row))
            opta = str(self._opta(row))
            print("betriebsstelle: ", betriebsstelle)

            excel_row = [
                row["tei"],
                    
                row["hersteller"],

                eg_typ,

                row["eg_art"],

                betriebsstelle,

                row["seriennummer"],

                "",

                "",

                "",

                "",

                "kA",

                "",

                "",

                "",

                "",
                
                "",
                    
                "",
                    
                "",
                    
                "",
                    
                "",
                    
                "",
                    
                "",
                    
                "",
                    
                "",
                    
                "",
                    
                "",
                    
                row["issi"],
                
                "kA",
                
                "",
                
                opta,
            ]
            self.ws.append(excel_row)
            written_rows.append(excel_row)

        self.wb.save(self.output_path)
        print(
            f"Excel-Datei erfolgreich generiert unter: {self.output_path.resolve()}"
        )

        return written_rows