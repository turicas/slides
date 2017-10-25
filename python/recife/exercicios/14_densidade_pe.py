import csv

arquivo = open('brasil.csv', encoding='utf8')
for registro in csv.DictReader(arquivo):
    if registro['estado'] == 'PE':
        densidade = int(registro['habitantes']) / float(registro['area'])
        print(f"{registro['municipio']}: {densidade}hab/km²")
