import csv

arquivo = open('brasil.csv', encoding='utf8')
populacao = 0
for registro in csv.DictReader(arquivo):
    estado = registro['estado']
    if estado == 'AL' or estado == 'BA' or estado == 'CE' or \
            estado == 'MA' or estado == 'PB' or estado == 'PE' or \
            estado == 'PI' or estado == 'RN' or estado == 'SE':
        populacao += int(registro['habitantes'])

print(f'O nordeste possui {populacao} habitantes.')
