import random

import nltk
from colorama import Fore, Back, Style
import us_abdo

import xlsxwriter
import ReportReader
import json


nltk.download('wordnet')
nltk.download('omw')
nltk.download('punkt')

print()

lang = 'fra'

reports = ReportReader.readReports("reports.txt")

# test text
facturations = []

workbook = xlsxwriter.Workbook('Report_results.xlsx')
worksheet = workbook.add_worksheet()

jsonList = []

# num = (int)(random.random() * 78)
for num in range(0, len(reports)):
    print(Back.GREEN + str(num) + Back.RESET)
    report = reports[num]
    (report, (facture, factureJson)) = us_abdo.cotation(report, lang)
    facturations.append([report, facture])
    jsonList.append({
        "title": "US Abdominal inférieur",
        "date": "00.00.0000",
        "status": "Not Reviewed",
        "report": report,
        "bill": factureJson
    },)
    worksheet.write(num, 0, report)
    worksheet.write(num, 1, facture)

workbook.close()

json_string = json.dumps(jsonList, indent=4)
with open('reports_result.json', 'w') as outfile:
    outfile.write(json_string)
