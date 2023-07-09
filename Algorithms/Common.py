import pandas


def readReports(filename):
    # read report in the db file
    f = open(filename, "r", encoding="utf-8")
    reports = f.readlines()
    f.close()
    return reports


def readRISExcel(filename):

    excel_data_df = pandas.read_excel(filename)

    print(excel_data_df)

    filteredSheet = excel_data_df[["Sexe Patient", "Date Examen",
                                   "Libelle Examen Parent", "Résultat"]]
    filteredSheet = filteredSheet.rename(columns={"Sexe Patient": "sexe", "Date Examen": "date",
                                                  "Libelle Examen Parent": "titre", "Résultat": "rapport"})

    dictSheet = filteredSheet.to_dict(orient="records")
    return dictSheet


def SplitDataByOrgans(tokened_sent):
    infos = []
    organes = []

    for sen in tokened_sent:
        splittedSen = sen.split(':')
        if (len(splittedSen) > 1):
            organes.append(splittedSen[0])
            infos.append(splittedSen[1])
        else:
            if (len(infos) != 0):
                infos[len(infos)-1] += sen
    organInfos = {}

    for i in range(0, len(infos)):

        organInfos[organes[i].lower().rstrip()] = infos[i]

    return organInfos


def unsplitDataByOrgans(organInfos):
    report = ""
    for key in organInfos:
        report += key+" : " + organInfos[key]
    return report
