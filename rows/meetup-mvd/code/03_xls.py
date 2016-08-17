import xlrd


def _convert_row(row):
    return [cell.value for cell in row]

def my_xls_reader(filename):
    workbook = xlrd.open_workbook(filename)
    sheet = workbook.sheet_by_index(0)
    header = _convert_row(sheet.row(0))
    for row_number in range(1, sheet.nrows):
        data = _convert_row(sheet.row(row_number))
        yield dict(zip(header, data))

filename = 'examples/data/tesouro-direto.xls'
for row in my_xls_reader(filename):
    print(row)
