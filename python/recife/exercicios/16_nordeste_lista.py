import csv

nordeste = ['AL', 'BA', 'CE', 'MA', 'PB', 'PE', 'PI', 'RN', 'SE']
arquivo = open('brasil.csv', encoding='utf8')
populacao = 0
for registro in csv.DictReader(arquivo):
    if registro['estado'] in nordeste:
        populacao += int(registro['habitantes'])

print(f'O nordeste possui {populacao} habitantes.')
