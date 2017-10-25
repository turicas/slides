import csv
from collections import Counter

norte = ['AC', 'AM', 'AP', 'PA', 'RO', 'RR', 'TO']
nordeste = ['AL', 'BA', 'CE', 'MA', 'PB', 'PE', 'PI', 'RN', 'SE']
centro_oeste = ['DF', 'GO', 'MS', 'MT']
sudeste = ['ES', 'MG', 'RJ', 'SP']
sul = ['PR', 'RS', 'SC']

arquivo = open('brasil.csv', encoding='utf8')
contador = Counter()
for registro in csv.DictReader(arquivo):
    estado = registro['estado']
    habitantes = int(registro['habitantes'])

    if estado in norte:
        contador['norte'] += habitantes
    elif estado in nordeste:
        contador['nordeste'] += habitantes
    elif estado in centro_oeste:
        contador['centro oeste'] += habitantes
    elif estado in sudeste:
        contador['sudeste'] += habitantes
    elif estado in sul:
        contador['sul'] += habitantes

print(f"Norte:        {contador['norte']}")
print(f"Nordeste:     {contador['nordeste']}")
print(f"Centro-Oeste: {contador['centro oeste']}")
print(f"Sudeste:      {contador['sudeste']}")
print(f"Sul:          {contador['sul']}")
