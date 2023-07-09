import pandas

excel_data_df = pandas.read_excel('excel_in.xls')

print(excel_data_df)

filteredSheet = excel_data_df[["Sexe Patient", "Date Examen",
                               "Libelle Examen Parent", "Résultat"]]

dictSheet = filteredSheet.to_dict(orient="records")

print(dictSheet[0])
