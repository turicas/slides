# coding: utf-8

from __future__ import unicode_literals

from io import BytesIO

import requests
import rows


url = 'http://cidades.ibge.gov.br/comparamun/compara.php?coduf=33&idtema=16&codv=v08'
resposta = requests.get(url)
html = resposta.content
with rows.locale_context('pt_BR.UTF-8'):
    tabela = rows.import_from_html(BytesIO(html))

for municipio in tabela:
    print municipio
