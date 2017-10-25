import csv

estado = input('Por qual estado gostaria de filtrar? ')
total = 0
arquivo = open('brasil.csv', encoding='utf8')
for registro in csv.DictReader(arquivo):
    if registro['estado'] == estado:
        total += int(registro['habitantes'])
print(f'Total para o estado {estado}: {total} habitantes.')
