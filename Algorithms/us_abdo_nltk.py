from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from nltk.stem import PorterStemmer
import random
from nltk.tokenize.treebank import TreebankWordDetokenizer
import os

import traceback
import nltk
from colorama import Fore, Back, Style

import Common

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


def cotation(report, lang):
    # split into sentences
    tokened_sent = sent_tokenize(report)

    organInfos = Common.SplitDataByOrgans(tokened_sent)

    # Check the presence of a Doppler
    doppler, report = _isDoppler(report)
    # post mictionnel

    miction, report = _isPostMictionnel(report)
    # Tube digestif

    tubeDigestif, report = _isTubeDigestif(report, organInfos, lang)

    # Parties molles
    partiesMolles, report = _isPartieMolles(report)

    renal, report = _isRenal(report)

    (inf, sup, comp, flag) = _isInfSupOrComplete(organInfos, lang)

    infos_facturation = [
        {
            "tarmed": {"code": "39.0010",
                       "description":  "Consultation de base/unité d'exploitation Institut de radiologie en dehors de l'hôpital"},
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
            "presence": tubeDigestif,
            "colorClass": 'bg-danger'

        },
        {
            "tarmed": partiesMollesCode,
            "presence": partiesMolles,
            "colorClass": 'bg-info'

        },
        {
            "tarmed": artereRenaleCode,
            "presence": renal,
            "colorClass": 'bg-primary'

        }


    ]

    return (report, _facturation(infos_facturation), flag)


def _facturation(info_facturation):
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


def _isDoppler(report):

    tokened_word = word_tokenize(report)
    doppler = False
    wordList = ['dopler', 'doppler',
                'sushépatique', 'sus-hépatique', 'hépatopète', 'vascularisé', 'veine']

    return _checkPresence(report, wordList, 'bg-warning')


def _isPostMictionnel(report):
    wordList = ['miction']

    return _checkPresence(report, wordList, 'bg-success')


def _isTubeDigestif(report, organInfos, lang):
    tubeDigestif = False

    try:
        infoDigestif = organInfos['tube digestif']
        if ('examen non dédié' not in infoDigestif):
            index = report.index('Tube digestif')
            newReport = report[:index] + \
                "<span class='bg-danger bg-opacity-50'>Tube digestif</span>" + \
                report[index+len('Tube digestif'):]
            return True, newReport

    except:
        pass
    return False, report


def _isPartieMolles(report):
    wordList = ['hernie', 'ligne blanche',
                'éventration' 'Valsalva', 'inguinal']

    return _checkPresence(report, wordList, 'bg-info')


def _isRenal(report):
    wordList = ['intraparenchymateux', 'vitesse systolique', 'pics systoliques',
                'systolique', 'index de résistance', 'index de résistivité',
                'analyse des flux', 'hile rénal', 'artère rénale hilaire',
                'anastomose']

    return _checkPresence(report, wordList, 'bg-primary')


def _isInfSupOrComplete(organInfos, lang):
    flag = False
    try:
        infosConstat = organInfos['autres constatations'].lower()
        isDefault = 'ne montre pas d’anomalie' in infosConstat
        isDefaultInguinal = 'pas d’anomalie supplémentaire.' in infosConstat
        isNone = 'aucune.' in infosConstat

        if (not (isDefault or isNone or isDefaultInguinal)):
            flag = True

    except:
        pass

    organes_sup = ['foie', 'rate', 'biliaire', 'pancréas']
    organes_inf = ['génitaux', 'vessie']
    sup = False
    inf = False
    comp = False

    organsInf = False
    organsSup = False
    keys = list(organInfos.keys())
    for i in range(0, len(keys)):
        keys[i] = keys[i].lower()

    for key in keys:
        for organe in organes_inf:
            if (organe in key):
                organsInf = True
        for organe in organes_sup:
            if (organe in key):
                organsSup = True
    inf = organsInf
    sup = organsSup
    if ((organsInf or organsSup) == False):
        inf = False
        sup = False
        comp = False
    if (organsInf and organsSup):
        # examen complet
        inf = False
        sup = False
        comp = True

    return (inf, sup, comp, flag)


def _checkPresence(report, wordList, colorClass):
    newReport = report
    presence = False
    checkReport = report.lower()

    for keyword in wordList:
        checkReport = newReport.lower()

        if (keyword in checkReport):
            index = checkReport.index(keyword)
            presence = True
            newReport = newReport[:index] + \
                "<span class='" + colorClass+" bg-opacity-50'>"+keyword+"</span>" + \
                newReport[index+len(keyword):]

    return (presence, newReport)
