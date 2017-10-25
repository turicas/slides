import csv
from collections import Counter

contador = Counter()
arquivo = open('brasil.csv', encoding='utf-8')
for registro in csv.DictReader(arquivo):
    contador[registro['estado']] += int(registro['habitantes'])

saida = csv.writer(
        open('habitantes-por-estado.csv', mode='w', encoding='utf8'),
        lineterminator='\n'
)
saida.writerow(['estado', 'habitantes'])
for estado, habitantes in contador.most_common():
    saida.writerow([estado, habitantes])
