import csv
import datetime

from decimal import Decimal


def _convert_float(data):
    return float(data)

def _convert_percent(data):
    mask = Decimal('0.0001')
    return float(Decimal(float(data.replace('%', '')) / 100).quantize(mask))

def _convert_date(data):
    date = datetime.datetime.strptime(data, '%Y-%m-%d')
    return datetime.date(date.year, date.month, date.day)

def _convert_datetime(data):
    return datetime.datetime.strptime(data, '%Y-%m-%dT%H:%M:%S')

def convert_row(row):
    row['preco_compra'] = _convert_float(row['preco_compra'])
    row['preco_venda'] = _convert_float(row['preco_venda'])
    row['taxa_compra'] = _convert_percent(row['taxa_compra'])
    row['taxa_venda'] = _convert_percent(row['taxa_venda'])
    row['vencimento'] = _convert_date(row['vencimento'])
    row['timestamp'] = _convert_datetime(row['timestamp'])

def my_csv_reader(fobj):
    for row in csv.DictReader(fobj):
        convert_row(row)
        yield row

filename = 'examples/data/tesouro-direto.csv'
reader = my_csv_reader(open(filename))
rows = list(reader)

preco_compra = [row['preco_compra'] for row in rows]
print('Media de preco_compra:', sum(preco_compra) / len(preco_compra))
