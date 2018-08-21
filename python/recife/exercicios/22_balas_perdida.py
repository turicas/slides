import csv
import requests

encontrados, nao_encontrados = 0, 0
materias = csv.DictReader(open('bala-perdida.csv', encoding='utf-8'))
for materia in materias:
    link = materia['link']
    print(f'Baixando {link}...')
    pagina = requests.get(link)

    if 'bala perdida' in pagina.text:
        print('Termo encontrado!')
        encontrados += 1
    else:
        print('Termo não encontrado')
        nao_encontrados += 1

print(f'Encontrados: {encontrados}')
print(f'Não encontrados: {nao_encontrados}')
