import csv
from collections import Counter

# Contando
contador_populacao = Counter()
contador_area = Counter()
arquivo = open('brasil.csv', encoding='utf-8')
for registro in csv.DictReader(arquivo):
    estado = registro['estado']
    habitantes = int(registro['habitantes'])
    area = float(registro['area'])

    contador_populacao[estado] += habitantes
    contador_area[estado] += area

# Criando o arquivo de saída
saida = csv.writer(
        open('densidade-por-estado.csv', mode='w', encoding='utf8'),
        lineterminator='\n'
)
saida.writerow(['estado', 'habitantes', 'area', 'densidade'])
for estado, habitantes in contador_populacao.most_common():
    area = contador_area[estado]
    densidade = habitantes / area
    saida.writerow([estado, habitantes, area, densidade])
