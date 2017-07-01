import csv

brasil = csv.DictReader(open('municipios-brasil.csv', encoding='utf-8'))

# Calcula total de habitantes por estado (armazena em um dicionário)
total = {}
for municipio in brasil:
        estado = municipio['estado']
        habitantes = int(municipio['habitantes'])
        if estado not in total:
                total[estado] = 0
        total[estado] = total[estado] + habitantes

# Salva resultado no arquivo "habitantes.csv"
arquivo = open('habitantes.csv', mode='w', encoding='utf-8')
resultado = csv.DictWriter(arquivo, fieldnames=['estado', 'habitantes'])
resultado.writeheader()
for sigla_estado, habitantes_estado in total.items():
        resultado.writerow({'estado': sigla_estado,
                            'habitantes': habitantes_estado})
