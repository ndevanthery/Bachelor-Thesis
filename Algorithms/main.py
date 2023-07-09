import random

import nltk
from colorama import Fore, Back, Style

import us_abdo_nltk
import us_abdo_spacy

import xlsxwriter
import Common
import json

import os

nltk.download('wordnet')
nltk.download('omw')
nltk.download('punkt')

print()

lang = 'fra'

# reports = Common.readReports("reports.txt")

reports = Common.readRISExcel("excel_in.xls")
os.system("Pause")

# test text
facturations = []

workbook = xlsxwriter.Workbook('Report_results.xlsx')
worksheet = workbook.add_worksheet()

cell_format = workbook.add_format()
cell_format.set_text_wrap()

jsonListNLTK = []
jsonListSpacy = []

usAbdo = us_abdo_spacy.UsAbdo()

# num = (int)(random.random() * 78)
for num in range(0, len(reports)):
    print(Back.GREEN + str(num) + Back.RESET)
    report = reports[num]["rapport"]
    (reportNLTK, (factureNLTK, factureJsonNLTK)
     ) = us_abdo_nltk.cotation(report, lang)
    (reportSpacy, (factureSpacy, factureJsonSpacy)) = usAbdo.cotation(report)

    facturations.append([report, factureNLTK, factureJsonSpacy])
    jsonListNLTK.append({
        "title": reports[num]["titre"],
        "date": reports[num]["date"].strftime("%d.%m.%Y"),
        "status": "Not Reviewed",
        "report": reportNLTK,
        "bill": factureJsonNLTK
    },)

    jsonListSpacy.append({
        "title": reports[num]["titre"],
        "date": reports[num]["date"].strftime("%d.%m.%Y"),
        "status": "Not Reviewed",
        "report": reportSpacy,
        "bill": factureJsonSpacy
    },)
    worksheet.write(num, 0, report, cell_format)
    worksheet.write(num, 1, factureNLTK, cell_format)
    worksheet.write(num, 2, factureSpacy, cell_format)

worksheet.autofit()
workbook.close()

json_stringNLTK = json.dumps(jsonListNLTK, indent=4)
json_stringSpacy = json.dumps(jsonListSpacy, indent=4)

with open('reports_result_NLTK.json', 'w') as outfile:
    outfile.write(json_stringNLTK)

with open('reports_result_SPACY.json', 'w') as outfile:
    outfile.write(json_stringSpacy)
