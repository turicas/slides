import csv

estado = input('Por qual estado gostaria de filtrar? ')
total = 0
arquivo = open('brasil.csv', encoding='utf8')
for registro in csv.reader(arquivo):
    if registro[0] == estado:
        total = total + int(registro[2])
print(total)
