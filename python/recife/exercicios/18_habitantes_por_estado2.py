import csv
from collections import Counter

contador = Counter()
arquivo = open('brasil.csv', encoding='utf8')
for registro in csv.DictReader(arquivo):
    contador[registro['estado']] += int(registro['habitantes'])

for estado, habitantes in contador.most_common(5):
    print(f'{estado} possui {habitantes} habitantes.')
