#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals, print_function

import shlex
import subprocess

from io import BytesIO
from urlparse import urljoin

import requests
import rows


URL_EDICAO = 'http://hemingway.softwarelivre.org/fisl{}/'
RESOLUCOES = ('low', 'high')
EDICOES = (11, 12, 13, 14, 15, 16)
COMANDO_DOWNLOAD = 'wget -c -t 3 {}'


def _baixa_listagem(url):
    html = requests.get(url).content
    tabela = rows.import_from_html(BytesIO(html))
    arquivos = [registro.name
                for registro in tabela if registro.name != 'Parent Directory']
    return arquivos


def _cria_url(edicao, resolucao, sala=None, arquivo=None):
    url = urljoin(URL_EDICAO.format(edicao), resolucao)
    if sala is not None:
        url += '/' + sala
        if arquivo is not None:
            url += '/' + arquivo
    return url


def baixa_videos_por_edicao(edicao, resolucao):
    if edicao not in EDICOES or resolucao not in RESOLUCOES:
        raise ValueError('Edição ou resolução inválida(s).')

    #print('Baixando lista de salas para fisl{}/{}...'
    #      .format(edicao, resolucao))
    url = _cria_url(edicao, resolucao)
    salas = [sala.replace('/', '')
             for sala in _baixa_listagem(url) if sala.endswith('/')]
    for sala in salas:
        baixa_videos_por_sala(edicao, resolucao, sala)


def baixa_videos_por_sala(edicao, resolucao, sala):
    #print('  Baixando lista de arquivos para fisl{}/{}/{}...'
    #      .format(edicao, resolucao, sala))

    url = _cria_url(edicao, resolucao, sala)
    arquivos = _baixa_listagem(url)
    for arquivo in arquivos:
        baixa_video(edicao, resolucao, sala, arquivo)


def baixa_video(edicao, resolucao, sala, arquivo):
    url = _cria_url(edicao, resolucao, sala, arquivo)
    #subprocess.call(shlex.split(COMANDO_DOWNLOAD.format(url)))
    print(COMANDO_DOWNLOAD.format(url))


if __name__ == '__main__':
    for edicao in EDICOES:
        baixa_videos_por_edicao(edicao, 'high')
