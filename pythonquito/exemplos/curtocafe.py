# coding: utf-8

from collections import namedtuple, OrderedDict
from decimal import Decimal
from io import BytesIO

import requests
import rows
import rows.fields


class PtBrCurrencyField(rows.fields.DecimalField):

    @classmethod
    def deserialize(cls, value, *args, **kwargs):
        if rows.fields.is_null(value):
            return None
        return Decimal(value.replace('R$', '').replace(',', '.').strip())


fields = OrderedDict([('produto', rows.fields.UnicodeField),
                      ('quantidade', rows.fields.IntegerField),
                      ('valor', PtBrCurrencyField),
                      ('', rows.fields.ByteField)])
fields_consumo = OrderedDict([('produto', rows.fields.UnicodeField),
                              ('quantidade', rows.fields.IntegerField),
                              ('valor_unitario', rows.fields.DecimalField),
                              ('valor_total', rows.fields.DecimalField)])
url_consumo = 'http://www.curto.coffee/contador/{data}/detalhes'


def html_consumo(data):
    """Retorna HTML de consumos no Curto Café para uma data (%Y-%m-%d)."""

    return requests.get(url_consumo.format(data=data)).content


def transforma(registro, tabela):
    return {'produto': registro.produto,
            'quantidade': registro.quantidade,
            'valor_unitario': registro.valor / registro.quantidade,
            'valor_total': registro.valor,}


def consumo_por_data(html, index=0):
    """Retorna lista de consumos no Curto Café para um HTML"""

    tabela = rows.import_from_html(BytesIO(html), index=index, fields=fields)
    return rows.transform(fields_consumo, transforma, tabela)


if __name__ == '__main__':
    html = html_consumo('2015-08-25')
    consumo1 = consumo_por_data(html, index=0)
    consumo2 = consumo_por_data(html, index=1)
