import csv
from collections import Counter

contador = Counter()
arquivo = open('brasil.csv', encoding='utf8')
for registro in csv.DictReader(arquivo):
    contador[registro['estado']] += int(registro['habitantes'])

print(contador.most_common(5))
