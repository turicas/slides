import csv

total = 0
arquivo = open('brasil.csv', encoding='utf8')
for registro in csv.reader(arquivo):
    total = total + int(registro[2])
print(total)
