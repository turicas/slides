import csv
import requests

notificacoes = list(csv.DictReader(open('notificacoes.csv')))

notificacoes_com_bala_perdida = []
notificacoes_sem_bala_perdida = []
total = len(notificacoes)
for contador, notificacao in enumerate(notificacoes, start=1):
    print('Baixando {} de {}'.format(contador, total))
    pagina = requests.get(notificacao['link'])

    if 'bala perdida' in pagina.text:
        notificacoes_com_bala_perdida.append(notificacao)
    else:
        notificacoes_sem_bala_perdida.append(notificacao)

print('As notificações com bala perdida são:')
for notificacao in notificacoes_com_bala_perdida:
    print(notificacao['link'])
print('Total {} de {}'.format(len(notificacoes_com_bala_perdida), total))
