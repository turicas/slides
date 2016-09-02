from lxml.html import document_fromstring


def _convert_row(row):
    values = row.xpath('.//th/text()') + row.xpath('.//td/text()')
    return [text.strip() for text in values]

def my_html_reader(filename):
    with open(filename) as fobj:
        tree = document_fromstring(fobj.read())
    tables = tree.xpath('//table')
    table = tables[0]
    rows = table.xpath('.//tr')
    header = _convert_row(rows[0])
    for row in rows[1:]:
        yield dict(zip(header, _convert_row(row)))

filename = 'examples/data/tesouro-direto.html'
for row in my_html_reader(filename):
    print(row)
