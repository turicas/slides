# coding: utf-8

from __future__ import print_function, unicode_literals

import datetime
import time

from collections import OrderedDict
from decimal import Decimal

import rows

from splinter import Browser


URL_CALCULADORA = 'http://www3.tesouro.gov.br/tesouro_direto/calculadora/calculadora_novosite.aspx'
CODIGOS_TITULOS = ('LTN', 'LFT', 'NTN-C', 'NTN-B', 'NTN-F', 'NTN-B Principal')
TITULOS_TAXA_GENERICA = ('LFT', 'NTN-C', 'NTN-B')


def formata_data(data):
    if type(data) is datetime.date:
        ano, mes, dia = data.year, data.month, data.day
    elif isinstance(data, basestring):
        ano, mes, dia = [int(info) for info in data.split('-')]
    else:
        raise ValueError('Formato de data inválido')
    return '{:02d}{:02d}{}'.format(dia, mes, ano)

def formata_valor(valor):
    return '{:.2f}'.format(valor).replace('.', ',')

def resultado_calculadora(codigo_titulo, data_compra, data_vencimento,
                          valor_investido, taxa_compra, taxa_administracao,
                          taxa_generica):
    browser = Browser('chrome')
    browser.visit(URL_CALCULADORA)
    browser.select('cbTitulo', codigo_titulo)
    while not browser.find_by_name('txtDtCompra'):
        time.sleep(0.1)
    browser.fill('txtDtCompra', formata_data(data_compra))
    browser.fill('txtDtVencimento', formata_data(data_vencimento))
    browser.fill('txtValorInvestido', formata_valor(valor_investido))
    browser.fill('txtTaxaCompra', formata_valor(taxa_compra))
    browser.fill('txtTaxaAdministracao', formata_valor(taxa_administracao))
    if codigo_titulo in TITULOS_TAXA_GENERICA:
        browser.fill('txtTaxaGenerica', formata_valor(taxa_generica))
    browser.find_by_name('btnCalcular').click()
    while 'RESULTADO DA SIMULAÇÃO' not in browser.html:
        time.sleep(0.1)
    html = browser.html
    browser.quit()
    return html

def formata_dinheiro(valor):
    valor = valor.replace('R$', '').replace('.', '').replace(',', '.').strip()
    return Decimal(valor)

def formata_percentual(valor):
    valor = valor.replace('%', '').replace('.', '').replace(',', '.').strip()
    return Decimal(valor) / 100

def parser_resultado(html):
    dados = html.split('<tbody>')[-1].split('</tbody>')[0]
    tabela_html = '''
    <table>
      <tr> <td>chave</td> <td>valor</td> </tr>
      {}
    </table>
    '''.format(dados)

    retorno = OrderedDict()
    for registro in rows.import_from_html(tabela_html):
        if registro.valor.startswith('R$'):
            valor = formata_dinheiro(registro.valor)
        elif '%' in registro.valor:
            valor = formata_percentual(registro.valor)
        else:
            valor = int(registro.valor)
        retorno[registro.chave] = valor

    return retorno

def calculadora(codigo_titulo, data_compra, data_vencimento, valor_investido,
                taxa_compra, taxa_administracao, taxa_generica=None):
    if codigo_titulo not in CODIGOS_TITULOS:
        raise ValueError('Código do título inválido')
    elif codigo_titulo in TITULOS_TAXA_GENERICA and taxa_generica is None:
        raise ValueError('Taxa genérica deve ser especificada para {}'
                         .format(codigo_titulo))

    html = resultado_calculadora(codigo_titulo, data_compra, data_vencimento,
                                 valor_investido, taxa_compra,
                                 taxa_administracao, taxa_generica)
    tabela = parser_resultado(html)
    return tabela


if __name__ == '__main__':

    resultado = calculadora('LTN', '2015-08-10', '2018-01-01', 5000, 13.9, 0.1)

    for chave, valor in resultado.items():
        print('{} => {}'.format(chave, valor))
