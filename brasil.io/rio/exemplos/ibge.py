# coding: utf-8

from __future__ import unicode_literals, print_function

import requests
import rows


URL_DADOS = 'http://cidades.ibge.gov.br/comparamun/compara.php'
INDICADORES = {'populacao': {'idtema': 16, 'codv': 'v08',},
               'area': {'idtema': 16, 'codv': 'v01',},}
CODIGO_UF = {'AC': 12, 'AL': 27, 'AM': 13, 'AP': 16, 'BA': 29, 'CE': 23,
             'DF': 53, 'ES': 32, 'GO': 52, 'MA': 21, 'MG': 31, 'MS': 50,
             'MT': 51, 'PA': 15, 'PB': 25, 'PE': 26, 'PI': 22, 'PR': 41,
             'RJ': 33, 'RN': 24, 'RO': 11, 'RR': 14, 'RS': 43, 'SC': 42,
             'SE': 28, 'SP': 35, 'TO': 17,}

def indicador_por_uf(indicador, uf):
    if uf not in CODIGO_UF:
        raise ValueError('UF "{}" inválido'.format(uf))
    elif indicador not in INDICADORES:
        raise ValueError('Indicador "{}" inválido'.format(indicador))

    parametros = INDICADORES[indicador].copy()
    parametros['coduf'] = CODIGO_UF[uf]
    resposta = requests.get(URL_DADOS, parametros)
    html = resposta.content.decode('utf-8')

    with rows.locale_context(('pt_BR', 'UTF-8')):
        tabela = rows.import_from_html(html)

    return tabela

if __name__ == '__main__':
    #for info in indicador_por_uf('populacao', 'RJ'):
    #    print('{} => {} habitantes'.format(info.municipio, info.pessoas))

    populacao_brasil = []
    for uf in CODIGO_UF:
        print('Baixando população para {}...'.format(uf))
        resultado = indicador_por_uf('populacao', uf)
        populacao_brasil.append(resultado)
    tabela_populacao_brasil = sum(populacao_brasil)
    rows.export_to_csv(tabela_populacao_brasil, 'populacao-brasil.csv')

    area_brasil = []
    for uf in CODIGO_UF:
        print('Baixando área para {}...'.format(uf))
        resultado = indicador_por_uf('area', uf)
        area_brasil.append(resultado)
    tabela_area_brasil = sum(area_brasil)
    rows.export_to_csv(tabela_area_brasil, 'area-brasil.csv')

    tabela_geral = rows.join(keys=('uf', 'municipio'),
                             tables=[tabela_populacao_brasil,
                                     tabela_area_brasil])
    rows.export_to_csv(tabela_geral, 'brasil.csv')
