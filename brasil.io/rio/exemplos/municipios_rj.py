# coding: utf-8

from __future__ import unicode_literals

import requests
import rows


url = 'http://cidades.ibge.gov.br/comparamun/compara.php?coduf=33&idtema=16&codv=v08'
resposta = requests.get(url)
html = resposta.content.decode('utf-8')
with rows.locale_context('pt_BR.UTF-8'):
    tabela = rows.import_from_html(html)

for municipio in tabela:
    print municipio
