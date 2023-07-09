
from colorama import Fore, Back, Style
import us_abdo

import xlsxwriter
import json


print()


def readReports(filename):
    # read report in the db file
    f = open(filename, "r", encoding="utf-8")
    reports = f.readlines()
    f.close()
    return reports


reports = readReports("reports.txt")
usAbdo = us_abdo.UsAbdo()


# test text
facturations = []

workbook = xlsxwriter.Workbook('Report_results.xlsx')
worksheet = workbook.add_worksheet()

jsonList = []

# num = (int)(random.random() * 78)
for num in range(0, len(reports)):
    print(Back.GREEN + str(num) + Back.RESET)
    report = reports[num]
    (report, (facture, factureJson)) = usAbdo.cotation(report)
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
