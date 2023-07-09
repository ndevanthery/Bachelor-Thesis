from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from nltk.stem import PorterStemmer
import random
from nltk.tokenize.treebank import TreebankWordDetokenizer

import traceback
import nltk
from colorama import Fore, Back, Style

import ReportReader


def cotation(report, lang):
    # split into sentences
    tokened_sent = sent_tokenize(report)

    # print report
    print(Back.RED + "REPORT" + Back.RESET + Fore.LIGHTCYAN_EX)
    for sen in tokened_sent:
        print(sen)
    # stop_words = set(stopwords.words('french'))

    # Split Data by organs / lines of the report

    organInfos = ReportReader.SplitDataByOrgans(tokened_sent)

    # print(organInfos)

    # Check the presence of a Doppler
    doppler, report = _isDoppler(report)
    # post mictionnel

    miction, report = _isPostMictionnel(report)
    # Tube digestif

    tubeDigestif, report = _isTubeDigestif(report, organInfos, lang)

    # Parties molles
    partiesMolles, report = _isPartieMolles(report)

    renal, report = _isRenal(report)

    (inf, sup) = _isInfSupOrComplete(organInfos, lang)

    return (report, _facturation(inf, sup, doppler, miction, tubeDigestif, partiesMolles, renal))


def _facturation(inf, sup, doppler, miction, tubeDigestif, partiesMolles, renal):
    facture = []
    fact = ""
    # simulation facture
    print(Back.RED + "Facture" + Back.RESET + Fore.GREEN)

    print("39.0010 - Consultation de base/unité d'exploitation Institut de radiologie en dehors de l'hôpital")
    fact += "39.0010 - Consultation de base/unité d'exploitation Institut de radiologie en dehors de l'hôpital\n"
    facture.append(
        {"code": "39.0010", "description":  "Consultation de base/unité d'exploitation Institut de radiologie en dehors de l'hôpital"})

    # prestation technique pour ultra son
    print("39.3800 - Prestation de base technique 0, grand examen par ultrasons, patient ambulatoire" + Fore.MAGENTA)
    fact += "39.3800 - Prestation de base technique 0, grand examen par ultrasons, patient ambulatoire\n"
    facture.append(
        {"code": "39.3800", "description":  "Prestation de base technique 0, grand examen par ultrasons, patient ambulatoire"})

    if (inf):
        print("39.3260 - Examen Trans abdominal par ultrasons du système uro-génital")
        fact += "39.3260 - Examen Trans abdominal par ultrasons du système uro-génital\n"
        facture.append(
            {"code": "39.3260", "description":  "Examen Trans abdominal par ultrasons du système uro-génital"})

    else:
        if (sup):
            print("39.3250 - US Abdo supérieur")
            fact += "39.3250 - US Abdo supérieur\n"
            facture.append(
                {"code": "39.3250", "description":  "US Abdo supérieur"})
        else:
            print(
                "39.3240 - Examen de l'ensemble de l'abdomen (supérieur et inférieur) par ultrasons ")
            fact += "39.3240 - Examen de l'ensemble de l'abdomen (supérieur et inférieur) par ultrasons \n"
            facture.append(
                {"code": "39.3240", "description":  "Examen de l'ensemble de l'abdomen (supérieur et inférieur) par ultrasons"})

    if (doppler):
        print("39.3510 - Sono des vaisseaux")
        fact += "39.3510 - Sono des vaisseaux\n"
        facture.append(
            {"code": "<span class='bg-warning bg-opacity-50'>39.3510</span>", "description":  "Sono des vaisseaux"})

    if (miction):
        print("39.3280 - Résidu post-mictionnel")
        fact += "39.3280 - Résidu post-mictionnel\n"
        facture.append(
            {"code": "<span class='bg-success bg-opacity-50'>39.3280</span>", "description":  "Résidu post-mictionnel"})

    if (tubeDigestif):
        print("39.3265 - Tube digestif")
        fact += "39.3265 - Tube digestif\n"
        facture.append(
            {"code": "<span class='bg-danger bg-opacity-50'>39.3265</span>", "description":  "Tube digestif"})

    if (partiesMolles):
        print("39.3420 - Parties molles")
        fact += "39.3420 - Parties molles\n"
        facture.append(
            {"code": "<span class='bg-info bg-opacity-50'>39.3420</span>", "description":  "Parties molles"})

    if (renal):
        print("39.3610 - Sonographie des artères rénales")
        fact += "39.3610 - Sonographie des artères rénales\n"
        facture.append(
            {"code": "<span class='bg-primary bg-opacity-50'>39.3610</span>", "description":  "Sonographie des artères rénales"})

    print(Fore.RESET + Back.RESET)
    return (fact, facture)


def _isDoppler(report):
    tokened_word = word_tokenize(report)
    doppler = False
    wordList = ['dopler', 'doppler',
                'sushépatique', 'sus-hépatique', 'hépatopète', 'vascularisé', 'veine']

    for index, w in enumerate(tokened_word):
        try:
            word = w.lower()
            for keyword in wordList:

                if (keyword in word):
                    doppler = True
                    tokened_word[index] = "<span class='bg-warning bg-opacity-50'>" + \
                        tokened_word[index]+"</span>"

        except:
            pass
    newReport = TreebankWordDetokenizer().detokenize(tokened_word)
    return (doppler, newReport)


def _isDopplerCopy(report, lang):
    tokened_word = word_tokenize(report)
    doppler_synset = wn.synsets('Doppler', lang=lang)[0]
    doppler = False

    for index, w in enumerate(tokened_word):
        try:
            word_synset = wn.synsets(w, lang=lang)[0]
            if (word_synset == doppler_synset):
                doppler = True
                tokened_word[index] = "<span class='bg-warning bg-opacity-50'>" + \
                    tokened_word[index]+"</span>"
        except:
            pass
    newReport = TreebankWordDetokenizer().detokenize(tokened_word)
    return (doppler, newReport)


def _isPostMictionnel(report):
    if ("miction" in report):
        index = report.index('miction')
        newReport = report[:index] + \
            "<span class='bg-success bg-opacity-50'>miction</span>" + \
            report[index+7:]
        return True, newReport

    return False, report


def _isTubeDigestif(report, organInfos, lang):
    tubeDigestif = False

    try:
        infoDigestif = organInfos['tube digestif']
        if ('examen non dédié' not in infoDigestif):
            index = report.index('Tube digestif')
            print(index)
            newReport = report[:index] + \
                "<span class='bg-danger bg-opacity-50'>Tube digestif</span>" + \
                report[index+len('Tube digestif'):]
            return True, newReport

    except:
        pass
    return False, report


""" def _isPartieMolles(report):
    tokened_word = word_tokenize(report)
    partiesMolles = False
    wordList = ['hernie', 'ligne blanche', 'éventration']

    for index, w in enumerate(tokened_word):
        try:
            word = w.lower()
            for keyword in wordList:

                if (keyword in word):
                    partiesMolles = True
                    tokened_word[index] = "<span class='bg-info bg-opacity-50'>" + \
                        tokened_word[index]+"</span>"

        except:
            pass
    newReport = TreebankWordDetokenizer().detokenize(tokened_word)
    return (partiesMolles, newReport) """


def _isPartieMolles(report):
    newReport = report
    partiesMolles = False
    wordList = ['hernie', 'ligne blanche',
                'éventration' 'Valsalva', 'inguinal']

    for keyword in wordList:

        if (keyword in newReport):
            index = newReport.index(keyword)
            partiesMolles = True
            newReport = newReport[:index] + \
                "<span class='bg-info bg-opacity-50'>"+keyword+"</span>" + \
                newReport[index+len(keyword):]

    return (partiesMolles, newReport)


def _isRenal(report):
    newReport = report
    renal = False
    wordList = ['intraparenchymateux', 'vitesse systolique', 'pics systoliques', 'systolique', 'index de résistance',
                'index de résistivité', 'analyse des flux', 'hile rénal', 'artère rénale hilaire', 'anastomose', 'intrarénale']

    for keyword in wordList:

        if (keyword in newReport):
            index = newReport.index(keyword)
            renal = True
            newReport = newReport[:index] + \
                "<span class='bg-primary bg-opacity-50'>"+keyword+"</span>" + \
                newReport[index+len(keyword):]

    return (renal, newReport)


def _isInfSupOrComplete(organInfos, lang):

    organes_sup = ['foie', 'rate', 'biliaire', 'pancréas']
    organes_inf = ['génitaux', 'vessie']
    sup = False
    inf = False

    inf_synset = wn.synsets('inférieur', lang=lang)[0]
    sup_synset = wn.synsets('supérieur', lang=lang)[0]
    try:
        infosConstat = organInfos['autres constatations']
        tokened_constat = word_tokenize(infosConstat)
        stop_words = set(stopwords.words('french'))

        filtered_sentence = [w for w in tokened_constat if w not in stop_words]
        for w in filtered_sentence:
            try:
                word_synset = wn.synsets(w, lang=lang)[0]

                if (word_synset == inf_synset):
                    sup = True
                if (word_synset == sup_synset):
                    inf = True
            except:
                pass
    except:
        """print(Back.WHITE + Fore.BLACK)
        print(list(organInfos.keys())) """
        for key in list(organInfos.keys()):
            for organe in organes_inf:
                if (organe in key):
                    inf = True
            for organe in organes_sup:
                if (organe in key):
                    sup = True
        if (inf & sup):
            # examen complet
            inf = False
            sup = False

    return (inf, sup)
