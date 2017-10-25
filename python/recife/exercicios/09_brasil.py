import csv

arquivo = open('brasil.csv', encoding='utf8')
for registro in csv.reader(arquivo):
    print(registro)
