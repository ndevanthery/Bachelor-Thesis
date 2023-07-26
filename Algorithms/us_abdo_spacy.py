import spacy
from spacy.matcher import Matcher
import os


consultationCode = {"code": "39.0010",
                    "description":  "Consultation de base/unité d'exploitation Institut de radiologie en dehors de l'hôpital"}

prestationBaseCode = {"code": "39.3800",
                      "description":  "Prestation de base technique 0, grand examen par ultrasons, patient ambulatoire"}

usInfCode = {"code": "39.3260",
             "description":  "Examen Trans abdominal par ultrasons du système uro-génital"}

usSupCode = {"code": "39.3250", "description":  "US Abdo supérieur"}

usCompletCode = {"code": "39.3240",
                 "description":  "Examen de l'ensemble de l'abdomen (supérieur et inférieur) par ultrasons"}
dopplerCode = {"code": "39.3510",
               "description":  "Sono des vaisseaux"}
postMictionnelCode = {"code": "39.3280",
                      "description":  "Résidu post-mictionnel"}
tubeDigestifCode = {
    "code": "39.3265", "description":  "Tube digestif"}
partiesMollesCode = {
    "code": "39.3420", "description":  "Parties molles"}

artereRenaleCode = {"code": "39.3610",
                    "description":  "Sonographie des artères rénales"}


class UsAbdo:

    def __init__(self):
        self.nlp = spacy.load("fr_core_news_lg")
        self.matcher = Matcher(self.nlp.vocab)
        """ patterns_sonoDesVaisseaux = [
            [{"lower": "doppler"}],
            [{"lower": "dopler"}],
            [{"lower": "sushépatique"}],
            [{"lower": "sushépatiques"}],
            [{"lower": "sus-hépatique"}],
            [{"lower": "sus-hépatiques"}],
            [{"lower": "hépatopète"}],
            [{"lower": "hépatofuge"}],
            [{"lower": "vascularisé"}],
            [{"lower": "vascularisée"}],
            [{"lower": "veine"}],
            [{"lower": "veines"}],
            [{"lower": "veine"}, {"lower": "porte"}],

        ]
        patterns_PostMictionnel = [
            [{"lower": "mictionnel"}],
            [{"lower": "miction"}],
            [{"lower": "prémictionnel"}],
            [{"lower": "postmictionnel"}],
        ]
        patterns_partiesMolles = [
            [{"lower": "hernie"}],
            [{"lower": "ligne"}, {"lower": "blanche"}],
            [{"lower": "éventration"}],
            [{"lower": "valsalva"}],
            [{"lower": "inguinal"}],

        ]
        patterns_renal = [
            [{"lower": "intraparenchymateux"}],
            [{"lower": "vitesse"}, {"lower": "systolique"}],
            [{"lower": "pics"}, {"lower": "systoliquse"}],
            [{"lower": "systolique"}],
            [{"lower": "index"}, {"lower": "de"}, {"lower": "résistance"}],
            [{"lower": "index"}, {"lower": "de"}, {"lower": "résistance"}],
            [{"lower": "analyse"}, {"lower": "des"}, {"lower": "flux"}],
            [{"lower": "hile"}, {"lower": "rénal"}],
            [{"lower": "artère"}, {"lower": "rénale"}, {"lower": "hilaire"}],
            [{"lower": "anastomose"}],
            [{"lower": "intrarénale"}],
        ]
        patterns_digest_non_dedie = [
            [{"lower": "tube"}, {"lower": "digestif"},
             {"OP": "*"},
             {"lower": "("}, {"lower": "examen"}, {"lower": "non"}, {
                "lower": "dédié"}, {"lower": ")"},
             ],]
        patterns_tube_digestif = [
            [{"lower": "tube"}, {"lower": "digestif"}
             ]
        ]
        patterns_usSup = [
            [{"lower": "foie"}],
            [{"lower": "rate"}],
            [{"lower": "voies"}, {"lower": "biliaires"}],
            [{"lower": "biliaire"}],
            [{"lower": "pancréas"}],

        ]
        patterns_usInf = [
            [{"lower": "organes"}, {"lower": "génitaux"}],
            [{"lower": "vessie"}],

        ]
        pattern_sup_pas_anomalie = [
            [{"lower": "abdomen"}, {"lower": "supérieur"}, {"lower": "ne"}, {
                "lower": "montre"}, {"lower": "pas"}, {"lower": "d’"}, {"lower": "anomalie"}],
        ]
        pattern_inf_pas_anomalie = [
            [{"lower": "abdomen"}, {"lower": "inférieur"}, {"lower": "ne"}, {
                "lower": "montre"}, {"lower": "pas"}, {"lower": "d’"}, {"lower": "anomalie"}],
        ]
        patterns_autre_constatations = [
            [{"lower": "autres"}, {"lower": "constatations"},
             ]
        ] """
        patterns_sonoDesVaisseaux = [
            [{"lower": {"FUZZY1": "doppler"}}],
            [{"lower": {"FUZZY1": "sushépatique"}}],
            [{"lower": {"FUZZY1": "hépatopète"}}],
            [{"lower": {"FUZZY1": "vascularisé"}}],
            [{"lower": {"FUZZY1": "veine"}}],

        ]

        patterns_PostMictionnel = [
            [{"lower": {"FUZZY1": "post-mictionnel"}}],
            [{"lower": {"FUZZY1": "pré-mictionnel"}}],
            [{"lower": {"FUZZY1": "mictionnel"}}],
            [{"lower": {"FUZZY1": "miction"}}],
        ]
        patterns_tube_digestif = [
            [{"lower": {"FUZZY1": "tube"}}, {"lower": {"FUZZY1": "digestif"}}
             ]
        ]

        patterns_digest_non_dedie = [
            [{"lower": {"FUZZY1": "tube"}}, {"lower": {"FUZZY1": "digestif"}}, {"IS_SPACE": True, "OP": "?"},
                {"IS_PUNCT": True, "OP": "?"}, {"IS_SPACE": True,
                                                "OP": "?"},  {"IS_ALPHA": True, "OP": "*"},
                {"lower": "("}, {"lower": {"FUZZY1": "examen"}}, {"lower": {"FUZZY1": "non"}}, {
                "lower": {"FUZZY1": "dédié"}}, {"lower": ")"},
             ],]

        patterns_partiesMolles = [
            [{"lower": {"FUZZY1": "hernie"}}],
            [{"lower": {"FUZZY1": "ligne"}}, {"lower": {"FUZZY1": "blanche"}}],
            [{"lower": {"FUZZY1": "éventration"}}],
            [{"lower": {"FUZZY1": "valsalva"}}],
            [{"lower": {"FUZZY1": "inguinal"}}],

        ]

        patterns_renal = [
            [{"lower": {"FUZZY1": "intraparenchymateux"}}],
            [{"lower": {"FUZZY1": {"IN": ["vitesse", "pics"]}}},
                {"lower": {"FUZZY1": "systolique"}}],
            [{"lower": "systolique"}],
            [{"lower": {"FUZZY1": "index"}}, {"lower": {"FUZZY1": "de"}}, {
                "lower": {"FUZZY1": {"IN": ["résistance", "résistivité"]}}},],
            [{"lower": {"FUZZY1": "analyse"}}, {
                "lower": {"FUZZY1": "des"}}, {"lower": {"FUZZY1": "flux"}}],
            [{"lower": {"FUZZY1": "hile"}}, {"lower": {"FUZZY1": "rénal"}}],
            [{"lower": {"FUZZY1": "artère"}}, {"lower": {"FUZZY1": "rénale"}},
                {"lower": {"FUZZY1": "hilaire"}}],
            [{"lower": {"FUZZY1": "anastomose"}}],
        ]

        patterns_usSup = [
            [{"lower": {"FUZZY1": "foie"}}],
            [{"lower": {"FUZZY1": "rate"}}],
            [{"lower": {"FUZZY1": "voies"}}, {"lower": {"FUZZY1": "biliaires"}}],
            [{"lower": {"FUZZY1": "biliaire"}}],
            [{"lower": {"FUZZY1": "pancréas"}}],


        ]
        patterns_usInf = [
            [{"lower": {"FUZZY1": "organes"}}, {"lower": {"FUZZY1": "génitaux"}}],
            [{"lower": {"FUZZY1": "vessie"}}],
        ]

        pattern_sup_pas_anomalie = [
            [{"lower": {"FUZZY1": "abdomen"}}, {"lower": {"FUZZY1": "supérieur"}},
             {"lower": {"FUZZY1": "ne"}}, {"lower": {"FUZZY1": "montre"}},
             {"lower": {"FUZZY1": "pas"}}, {"lower": {"FUZZY1": "d’"}}, {
                "lower": {"FUZZY1": "anomalie"}}
             ]
        ]
        pattern_inf_pas_anomalie = [
            [{"lower": {"FUZZY1": "abdomen"}}, {"lower": {"FUZZY1": "inférieur"}},
             {"lower": {"FUZZY1": "ne"}}, {"lower": {"FUZZY1": "montre"}},
             {"lower": {"FUZZY1": "pas"}}, {"lower": {"FUZZY1": "d’"}}, {
                "lower": {"FUZZY1": "anomalie"}}
             ]
        ]
        patterns_autre_constatations = [
            [{"lower": {"FUZZY1": "autres"}}, {"lower": {"FUZZY1": "constatations"}},
             ]
        ]
        self.matcher.add("SONO_DES_VAISSEAUX", patterns_sonoDesVaisseaux)
        self.matcher.add("RESIDU_POSTMICTIONNEL", patterns_PostMictionnel)
        self.matcher.add("PARTIES_MOLLES", patterns_partiesMolles)
        self.matcher.add("SONO_ARTERE_RENALE", patterns_renal)
        self.matcher.add("US_INF", patterns_usInf)
        self.matcher.add("US_SUP", patterns_usSup)
        self.matcher.add("US_INF_ANOMALIE", pattern_sup_pas_anomalie)
        self.matcher.add("US_SUP_ANOMALIE", pattern_inf_pas_anomalie)
        self.matcher.add("TUBE_DIGESTIF_NON_DEDIE", patterns_digest_non_dedie)
        self.matcher.add("TUBE_DIGESTIF_SECTION", patterns_tube_digestif)
        self.matcher.add("AUTRES_CONSTATATION_SECTION",
                         patterns_autre_constatations)

    def _facturation(self, info_facturation):
        facture = []
        fact = ""

        for position in info_facturation:
            if (position["presence"]):
                tm = {
                    "code": position["tarmed"]["code"],
                    "description": position["tarmed"]["description"],
                }
                print(tm["code"] + " - " + tm["description"])
                fact += tm["code"] + " - " + tm["description"] + '\n'
                if (position["colorClass"] != None):
                    code = tm['code']
                    annotatedCode = "<span class='"+position['colorClass'] + \
                        " bg-opacity-50'>" + code+"</span>"
                    facture.append(
                        {"code": annotatedCode, "description": tm["description"]})
                else:
                    facture.append(tm)

        return (fact, facture)

    def cotation(self, report):
        doc = self.nlp(report)
        matches = self.matcher(doc)

        # for token in doc:
        #    print(token.text)
        # presence variables
        doppler = False
        miction = False
        part_molles = False
        art_renale = False
        tube_digestif = False

        us_inf = False
        us_sup = False
        autre_constat = False
        us_sup_sans_anomalie = False
        us_inf_sans_anomalie = False

        # Iterate over the matches and print the span text
        for match_id, start, end in matches:

            # Get string representation
            string_id = self.nlp.vocab.strings[match_id]
            if string_id == "SONO_DES_VAISSEAUX":
                doppler = True
            if string_id == "RESIDU_POSTMICTIONNEL":
                miction = True
            if string_id == "PARTIES_MOLLES":
                part_molles = True
            if string_id == "SONO_ARTERE_RENALE":
                art_renale = True
            if string_id == "US_INF":
                us_inf = True
            if string_id == "US_SUP":
                us_sup = True
            if string_id == "AUTRES_CONSTATATION_SECTION":
                autre_constat = True
            if string_id == "US_INF_ANOMALIE":
                us_inf_sans_anomalie = True
            if string_id == "US_SUP_ANOMALIE":
                us_sup_sans_anomalie = True
            if string_id == "TUBE_DIGESTIF_SECTION":
                tube_digestif = True
            if string_id == "TUBE_DIGESTIF_NON_DEDIE":
                tube_digestif = False

            # print(string_id, doc[start:end])

        # span = doc[start: end]
        inf = False
        sup = False
        comp = False
        if (us_inf & us_sup == True):
            comp = True
        else:
            if (us_inf):
                if (us_inf_sans_anomalie or (not (autre_constat))):
                    inf = True
                else:
                    comp = True
            if (us_sup):
                if (us_sup_sans_anomalie or (not (autre_constat))):
                    sup = True
                else:
                    comp = True

        infos_facturation = [
            {
                "tarmed": consultationCode,
                "presence": True,
                "colorClass": None
            },
            {
                "tarmed": prestationBaseCode,
                "presence": True,
                "colorClass": None

            },
            {
                "tarmed": usInfCode,
                "presence": inf,
                "colorClass": None

            },
            {
                "tarmed": usSupCode,
                "presence": sup,
                "colorClass": None

            },
            {
                "tarmed": usCompletCode,
                "presence": comp,
                "colorClass": None

            },
            {
                "tarmed": dopplerCode,
                "presence": doppler,
                "colorClass": 'bg-warning'

            },
            {
                "tarmed": postMictionnelCode,
                "presence": miction,
                "colorClass": 'bg-success'

            },
            {
                "tarmed": tubeDigestifCode,
                "presence": tube_digestif,
                "colorClass": 'bg-danger'

            },
            {
                "tarmed": partiesMollesCode,
                "presence": part_molles,
                "colorClass": 'bg-info'

            },
            {
                "tarmed": artereRenaleCode,
                "presence": art_renale,
                "colorClass": 'bg-primary'

            }


        ]
        return (report, self._facturation(infos_facturation))


""" usAbdo = UsAbdo()
text = "EchographieFoie   :   taille normale ; hyperéchogénicité diffuse du parenchyme avec visibilité réduite des segments dorsaux. Pas de lésion focale. Veine porte non évaluable.Voies biliaires   :   de calibre normal. Vésicule de parois fines sans calcul décelable.Pancréas   :   d'analyse limitée en raison d'interpositions de l'intestin.Rate   :   de taille normale, homogène. Reins   :   de morphologie normale, sans dilatation des cavités.Rétropéritoine   :   pas d’adénopathies ni de masse. Aorte de calibre normal.Tube digestif   :   sans anomalie grossière (examen non dédié).Péritoine   :   pas de liquide libre.Vessie   :   très peu remplie.Organes génitaux   :   non visualisés.Radiographies Silhouette cardiaque    :   sans élargissement, index cardio-thoracique dans la norme.Médiastin et hiles    :   sans image de masse. Port-a-Cath pectoral droit. Poumons   :   aération symétrique, pas d’infiltrat ni d’opacités. Lobe azygos.Plèvre    :   pas d’épanchement.Squelette    :   spondylose antérieure étagée thoracique moyenne.Autres   :   pas d’anomalie des parties molles. "
text = text.replace(".", ". ")
print(text)
usAbdo.cotation(text)
 """
