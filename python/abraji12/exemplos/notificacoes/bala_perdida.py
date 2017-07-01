import csv
import requests

encontrou = 0
nao_encontrou = 0
notificacoes = csv.DictReader(open('notificacoes.csv', encoding='utf-8'))
for notificacao in notificacoes:
    pagina = requests.get(notificacao['link'])
    if 'bala perdida' in pagina.text:
        print(notificacao['link'])
        encontrou = encontrou + 1
    else:
        print('nao encontrado')
        nao_encontrou = nao_encontrou + 1

print('encontrados:', encontrou)
print('nao encontrados:', nao_encontrou)
